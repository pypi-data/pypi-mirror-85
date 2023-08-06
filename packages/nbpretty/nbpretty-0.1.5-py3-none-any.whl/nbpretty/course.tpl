{% extends 'full.tpl' %}

{%- block html_head -%}
{{ super() }}
<meta name="viewport" content="width=device-width, initial-scale=1">
{%- endblock html_head -%}

{% block body %}
<body>
  <div tabindex="-1" id="notebook" class="border-box-sizing">
    <div class="container" id="notebook-container">
    <h1 id="main-title">{{ nb.metadata.course_title }}</h1>
{{ super.super() }}
    </div>
  </div>
</body>
{%- endblock body %}

{% block markdowncell %}
<div class="cell border-box-sizing text_cell rendered{% if cell.custom_class %} {{ cell.custom_class }}{% endif %}">
{%- if cell.metadata.custom_block is defined -%}
<input type="checkbox" id="custom_block{{ cell.metadata.custom_block.id }}" class="custom_block_checkbox" checked>
<div class="prompt custom_block_prompt">
    <label for="custom_block{{ cell.metadata.custom_block.id }}"><img src="{{ cell.metadata.custom_block.image }}" class="icon"></label>
</div>
{%- elif resources.global_content_filter.include_input_prompt-%}
    {{ self.empty_in_prompt() }}
{%- endif -%}
<div class="inner_cell{% if cell.metadata.custom_block is defined %} collapsible{%- endif -%}">
<div class="text_cell_render border-box-sizing rendered_html">
{{ cell.source  | markdown2html | strip_files_prefix }}
</div>
</div>
</div>
{% endblock markdowncell %}

{% block in_prompt -%}
<div class="prompt input_prompt">
    {%- if cell.metadata.writefile is defined -%}
        {{ cell.metadata.writefile }}
    {%- elif cell.metadata.runcommand is defined -%}
        $
    {%- elif cell.execution_count is defined -%}
        In&nbsp;[{{ cell.execution_count|replace(None, "&nbsp;") }}]:
    {%- else -%}
        In&nbsp;[&nbsp;]:
    {%- endif -%}
</div>
{%- endblock in_prompt %}
