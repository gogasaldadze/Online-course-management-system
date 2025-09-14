
Brief overview:

i decided to accumulate all db models together in content dir in order to avoid migration madness. therefore we will be able to simply track our migration history since it wont be splitted among different apps. however i keep isolated Custom user model alongside with custom manager in access dir, which is responsible to asign profile accordingly (student or teacher). this is because its not really related to our business logic, its something more essential, specifically related to project.
lastly, regarding models, i love having Abstractmodel in common dir for my dbmodels even for our custom User model, because it provides essential data for each row created, such as UUID, created_at, updated_at, ordering and its not really model since we declare as abstract in Meta.

Instead of installing apps separately i prefer having my main API which contains sub-apis and gathers all sub urls to our API urls.py and we simply register every business logic related urls to our project under api/ endpoint. 
sub-apis of API contain needed files such as views, serializers, querysets etc.

Since we run our project on container and also for security purposes i keep hidden our SECRET_KEY, JWT related keys, oyur postgre creds and url.  Therefore in settings.py every important data is implied by help of ENV, .env and dj_database_url. 


    https://docs.astral.sh/uv/guides/integration/docker
    https://github.com/astral-sh/uv-docker-example/blob/main/Dockerfile

you may see i use different port 5436 on my local machine and this is because 5432 is kept by some process which i was not really able to terminate.


Lastly, want to mention makefile, because it rly saves my nerves and time :D and you may already have it, but still incase, i keep windows isntallation instruction below, because at first it was rly struggle to install this tool on win. 


windows installation: 
run in powershell as an administrator:

    1.
        Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   
    2.
        choco install make


quickstart:
            run: 
                make up  - >  make migrations - > make migrate - > make populate  -> make superuser (optional)
            
            optionally you can:  make clean   # remove cache and temporary files



to simplify process i pushed .env file, so you don't need to manually provide creds.

You can Register via using endpoint api/auth/register

I suggest you to use DRF templates to smoothlly navigate (also simple for swtiching users (teacher/student), since drf login presented) 

or use already existed creds:

        User Credentials

        Teachers
        Username	Password
        tch1	tch1pass
        tch2	tch2pass
        tch3	tch3pass
        tch4	tch4pass
        tch5	tch5pass
        tch6	tch6pass
        tch7	tch7pass
        tch8	tch8pass
        tch9	tch9pass
        tch10	tch10pass

        Students
        Username	Password
        std1	std1pass
        std2	std2pass
        std3	std3pass
        std4	std4pass
        std5	std5pass
        std6	std6pass
        std7	std7pass
        std8	std8pass
        std9	std9pass
        std10	std10pass







 



