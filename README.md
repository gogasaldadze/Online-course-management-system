Project is running on docker with using Postgre db. 

For running commands i am using makefile.

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