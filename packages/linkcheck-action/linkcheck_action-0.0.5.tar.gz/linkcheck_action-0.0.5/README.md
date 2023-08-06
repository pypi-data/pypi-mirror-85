# Title



## Linkcheck GitHub Action

These are small utlities built with [PyGitHub](https://github.com/PyGithub/PyGithub), and are designed to work inside [GitHub Actions](https://docs.github.com/en/free-pro-team@latest/actions).

The argument `token` is only required for private repositories.  You can [create a personal access token](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token), or use the [GITHUB_TOKEN](https://docs.github.com/en/free-pro-team@latest/actions/reference/authentication-in-a-workflow#about-the-github_token-secret) environment variable if using GitHub Actions.  **It is highly recommended to supply a token to obtain a more generous rate limit from the GitHub API.**

There are two ways to get a repository. You can specify the `{owner}/{repo}`:

```python
get_repo('fastai/fastai')
```




    Repository(full_name="fastai/fastai")



Or you can set the `GITHUB_REPOSITORY` environment variable, which also happens to be [set for you](https://docs.github.com/en/free-pro-team@latest/actions/reference/environment-variables) in GitHub Actions.

```python
os.environ['GITHUB_REPOSITORY'] = 'fastai/fastlinkcheck'
test_eq(get_repo().full_name,'fastai/fastlinkcheck')
```

```python
get_issues('fastai/fastcore')
```




    [Issue(title="store_attr doesn't work with Keyword-Only Arguments", number=193),
     Issue(title="Proposition: optional override to is_instance(x,t) to support both types and str in the same function", number=191),
     Issue(title="Fix test eq type for inner type", number=189),
     Issue(title="Fix pandas test eq", number=188),
     Issue(title="Remove `Param` and replace with param comments", number=186),
     Issue(title="Example: storing kwargs with store_attr", number=180),
     Issue(title="Latest FASTCORE version error: TypeError: patch() got an unexpected keyword argument 'as_prop'", number=177),
     Issue(title="Add default arguments to delegation", number=175),
     Issue(title="L(x, use_list=None) doesn't make a list if x is a numpy.float64", number=143),
     Issue(title="Pipeline setup not working as intended", number=141),
     Issue(title="support for optional params", number=88)]



```python
brokenlink_issue('_example/', ghtoken=os.getenv('GITHUB_TOKEN'), title='foo')
```


    ---------------------------------------------------------------------------

    AssertionError                            Traceback (most recent call last)

    <ipython-input-19-612a203d1260> in <module>
    ----> 1 brokenlink_issue('_example/', ghtoken=os.getenv('GITHUB_TOKEN'), title='foo')
    

    <ipython-input-18-59b33f3d0236> in brokenlink_issue(path, ghtoken, host, config_file, title)
         10     repo = os.getenv('GITHUB_REPOSITORY')
         11     token = ifnone(ghtoken, os.getenv('INPUT_TOKEN'))
    ---> 12     assert token, "You must supply a token or set the environment variable `INPUT_TOKEN`"
         13     assert repo, "You must set the environment variable `GITHUB_REPOSITORY` if running this outside Actions."
         14     l = link_check(path=path, host=host, config_file=config_file, actions_output=True, print_logs=True)


    AssertionError: You must supply a token or set the environment variable `INPUT_TOKEN`


```python
import os
```
