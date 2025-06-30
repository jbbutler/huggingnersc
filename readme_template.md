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

The following code can be used to access the dataset from its stored location at NERSC. You may also access this code via a NERSC-hosted Jupyter notebook [here](https://jupyter.nersc.gov/hub/user-redirect/lab/tree/global/cfs/cdirs/dasrepo/ai_ready_datasets/{{ nickname }}/{{ nickname }}_dataloader.ipynb).

```
{{ loading_code }}
```

*Note: this code assumes your working directory is the location of the dataset at NERSC: {{ nersc_loc }}*