# Stop/Start AWS environments
This package stops and starts AWS environments (group of instances according to tags) from an external scheduler

** Usage example:** Add Jenkins project to shutdown AWS qa environment for night and weekend
### Dependencies and prerequisites
- AWS credentials - located at ~/.aws/credentials on Linux, macOS, or Unix, or at C:\Users\USERNAME \.aws\credentials on Windows. This file can contain multiple named profiles in addition to a default profile.
- AWS config – typically located at ~/.aws/config on Linux, macOS, or Unix, or at C:\Users\USERNAME \.aws\config on Windows. This file can contain a default profile, named profiles, and CLI specific configuration parameters for each.

See further details [here](http://boto.cloudhackers.com/en/latest/boto_config_tut.html)

### Running the package from Jenkins/CLI
- Using pip:
  - pip install configAWSEnv
- calling the function: 
  - configAWSEnv -t/--tags <list of tags to filter> -a/--actions <SHUTDOWN/WAKEUP>
  - example: configAWSEnv --action WAKEUP --tags  environment=dev --tags service=service1* --tags nightly_shutdown=true

>### Development
>- prerequisite:
>  - Python 3.6
>  - virtualenv
>  - pybuilder
  
> ### run
> - checkout project
> - install virtualenv: 
>   - pip install virtualenv
>   - virtualenv -p python3.6 venv
>   - source venv/bin/activate
> - install pybuilder and project dependencies:
>   - pip install pybuilder
>   - pyb install_dependencies
>   - pyb -t (for further actions)
>   - pyb install



