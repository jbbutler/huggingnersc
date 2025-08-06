---
{% for field_name, field_entry in datacard_tags.items() -%}
{% if field_name=='pretty_name' -%}
{{field_name}}: {{field_entry}}
{% else -%}
{{field_name}}:
{% for item in (field_entry if field_entry is not string else [field_entry]) -%}
- {{ item }}    
{% endfor -%}
{% endif -%}
{% endfor -%}
---

# {{ datacard_tags.pretty_name }}

The following code can be used to load the dataset from its stored location at NERSC.

{% if not distributed -%}
You may also access this code via a NERSC-hosted Jupyter notebook [here](https://jupyter.nersc.gov/hub/user-redirect/lab/tree{{nersc_loc}}{{ other_info.nickname }}_dataloader.ipynb).
{% else -%}
{% endif -%}

{% if batch_code -%}
Batch script to run the dataloader.
```
{{ batch_code }}
```
{% endif -%}

```
{{ loading_code }}
```

If you would like to download the data, visit the following link:

{{ download_link }}