---
language:
- {{ language }}
tags:
{% for tag in tags -%}
- {{ tag }}
{% endfor -%}
pretty_name: {{ official_name }}
size_categories:
- {{ size_bucket }}
---

# {{ official_name }}

The following code can be used to load the dataset from its stored location at NERSC. You may also access this code via a NERSC-hosted Jupyter notebook [here](https://jupyter.nersc.gov/hub/user-redirect/lab/tree{{nersc_loc}}{{ nickname }}_dataloader.ipynb).

```
{{ loading_code }}
```

If you would like to download the data, visit the following link:

{{ download_link }}