# Copyright (c) 2020, Palo Alto Networks
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# Author: Andrew Mallory amallory@paloaltonetworks.com

import yaml
from jinja2 import Template
from jsonpath_rw import parse as jsonpath_parse
import json
import os
import datetime
import copy
import base64

class Report:
    
    def __init__(self, report_path):
        self.report_path = report_path if report_path.endswith('/') else report_path + '/'
        self.lib_path = os.path.dirname(os.path.abspath(__file__))
        self.__search_path = [ self.report_path, self.lib_path + '/primitives' ]
        self.template = None
        self.html = None
        self.data = {} # Input variables
        self.header_data = {}
        self.time_generated = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__load_template()
        self.__import_template()
        self.__expand_template()
        self.title = self.template['report']['title']
        self.subtitle = self.template['report']['subtitle']

    def __load_template(self):
        report_file = self.report_path + 'report.yml'
        with open(report_file, 'r') as f:
            self.template = yaml.safe_load(f)
    
    def __import_template(self):
        import_source = self.template.pop('import', None)
        if import_source:

            # Store the loaded file and override self.template
            override = copy.deepcopy(self.template)
            import_dir = os.path.normpath(os.path.join(self.report_path, import_source))
            import_path = os.path.join(import_dir, 'report.yml')
            if not os.path.exists(import_path):
                raise FileNotFoundError('Imported file - ' + import_source)
            with open(import_path, 'r') as f:
                self.template = yaml.safe_load(f)
            
            # Override the newly loaded template with values from old file
            for root_element in ['pre_processing', 'content_templates']:
                if root_element in override:
                    self.template[root_element] = override[root_element]
            self.template['report'].update(override['report'])

            # Sets the search precedence to specified dir, imported dir, included with doculib
            self.__search_path.insert(1, import_dir)
    
    def __expand_template(self):
        for section in self.template['report']['sections']:
            for content in section['content']:
                if 'template' in content:
                    template_name = content.pop('template')
                    var_override = copy.deepcopy(content)
                    updated_content = copy.deepcopy(self.template['content_templates'][template_name])
                    content.update(updated_content)
                    content.update(var_override)
        
    def load_data(self, data):
        self.data.update(data)
    
    def load_header(self, data):
        self.header_data.update(data)
    
    def __find_asset(self, name, ext=True):
        """
        ext is match file extention
        """
        for directory in self.__search_path:
            for file_name in os.listdir(directory):
                if not ext and file_name.split('.')[:1][0] == name or file_name == name:
                    return directory + '/' + file_name

    def __load_jinja_template(self, name):
        with open(name, 'r') as f:
            return Template(f.read())

    def __load_primitive(self, name):
        return self.__load_jinja_template('primitives/' + name)
    
    def __render_primitive(self, name, data):
        primitive_name = name if name.endswith('.j2') else name + '.j2'
        primitive_path = self.__find_asset(primitive_name)
        template = self.__load_jinja_template(primitive_path)
        return template.render(data)
    
    def __render_template(self, name):
        template_name = name if name.endswith('.j2') else name + '.j2'
        template_path = self.report_path + '/' + template_name
        with open(template_path, 'r') as f:
            t = Template(f.read())
        return t.render({})
    
    def __render_title(self):
        self.html += self.__render_primitive(
            'title',
            {
                'title': self.title,
                'subtitle': self.subtitle,
                'time_generated': self.time_generated,
                'meta': self.header_data
            }
        )
    
    def __render_css(self):
        self.html += '<style>'
        for directory in self.__search_path:
            for file_name in os.listdir(directory):
                if file_name.endswith('.css'):
                    with open(directory + '/' + file_name, 'r') as f:
                        self.html += f.read()
                elif file_name.startswith('icon-') and file_name.endswith('.svg'):
                    self.__load_icon(directory + '/' + file_name)
        self.html += '</style>'
    
    def __load_icon(self, icon_file):
        icon_name = '-'.join(icon_file.split('/')[-1].split('.')[0].split('-')[1:])
        with open(icon_file, 'r') as f:
            icon_data = f.read()
        icon_data = icon_data.replace('\n', '').replace('\t', '')
        self.html += '.icon-' + icon_name + '{'
        self.html += f"background: url('data:image/svg+xml;utf8,{icon_data}');"
        self.html += 'background-repeat: no-repeat; background-size:25px 25px; background-position: center; }\n'

    def __render_section(self, section):
        rHtml = self.__render_primitive('section_head', section)
        rHtml += '<div class="sec">'
        for content in section['content']:
            data = self.data
            if 'key' in content:
                data = jsonpath_parse(content['key']).find(self.data)[0].value
            context = {
                'data': data,
                'meta': content
            }
            rHtml += self.__render_primitive(content['type'], context)
        rHtml += '</div>'
        return rHtml

    def __render_sections(self):
        sections = self.template['report']['sections']
        for section in sections:
            self.html += self.__render_section(section)

    def __load_encoded_image(self, image_file):
        with open(image_file, 'rb') as f:
            logo_bytes = f.read()
        return base64.b64encode(logo_bytes).decode()

    def __render_logo(self, primitive='header', data={}):
        logo_file = self.__find_asset('logo', ext=False)
        logo_data = {
            'logo_ext': logo_file.split('.')[-1],
            'encoded_logo': self.__load_encoded_image(logo_file)
        }
        second_logo_file = self.template['report'].get('second_logo')
        if second_logo_file:
            second_logo_file = self.__find_asset(second_logo_file, ext=False)
            logo_data['second_logo_ext'] = second_logo_file.split('.')[-1]
            logo_data['second_encoded_logo'] = self.__load_encoded_image(second_logo_file)
        
        logo_data.update(data)
        logo_data['logo_style'] = self.template['report'].get('logo_style')
        logo_data['second_logo_style'] = self.template['report'].get('second_logo_style')
        logo_data['footer_links'] = self.template['report'].get('footer_links')
        self.html += self.__render_primitive(primitive, logo_data)

    def __pre_process_data(self):
        pre_template = Template(self.template['pre_processing'])
        rendered_text = pre_template.render(data=self.data)
        self.data = json.loads(rendered_text)

    def render_html(self):
        if 'pre_processing' in self.template:
            self.__pre_process_data()
        self.html = '<!DOCTYPE html><html>'
        self.html += self.__render_primitive(
            'html_head',
            {'title': self.title}
        )
        self.__render_css()
        self.html += '<body>'
        self.__render_logo()
        self.__render_title()
        self.__render_sections()
        self.__render_logo(primitive='footer')
        self.html += '</body></html>'
        return self.html