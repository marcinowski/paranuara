# National Population Institute of Paranuara API

To Mr Checktoporov, the President of Paranuara.

# Prologue

After 10 years of rapid development this once deserted planet has become one of the most prosperiting places of our great nation.
The task you've hired me for was not easy, but I believe that my hard work will please your expectations. It was a great pleasure
to work with new technologies I've never had an opportunity to work with. MongoDB for example, Mr President, why haven't our great nation
used it before! My rough beginner approach to the topic seems to be working, but it looks like there's a lot to improve in 
this field. I believe that my work will be the first step to better understanding of this piece of engineering and an occasion to improve 
our older systems as well! Below you'll find a walk through that will guide you throughout the system I've created.

# Chapter 1 - Set Up

Dear Mr President, to set up this project, please make sure for your own comfort:
 - that you're using Python 3 and path to `python` and `virtualenv` executable is added to your environmental PATH
 - that you have installed MongoDB and `mongo`, as well as `mongod` paths are also added to PATH
 - if your computer works inside a local network behind a proxy, set appropriate `http_proxy` variables.
 - nothing is running on your port 27017 except MongoDB server
 - you are in the root directory (above `src`) (for explanation see *Note* below)

After you've made sure that you fulfill all these requirements you should simply run:
 - `. setup.sh` on Linux/Unix based environment
 - or `setup.cmd` if you're using Windows.
 
*Note: after moving to Paranuara, I lost my Linux environment and wasn't able to put it back on such a 
short notice. The Windows script is tested and works on my setup, however Linux is not properly tested although 
also should work when run from root directory (above `src` directory).*

These commands will:
 - verify your Python version
 - setup an virtualenv to work on
 - install all project dependencies
 - set up a database in mongoDB
 - run `mongod` server on port 27017
 - populate the database with data provided by you
 - run simple local server for data presentation on `localhost:8000` or `127.0.0.1:8000`

Setup may take up to 5 minutes depending on your network connection and hardware.

# Chapter 2 - Catch

Application I've created is based on Django - Django Rest Framework - MongoDB setup. 
It enables to quickly view all the companies and employees from planet Paranuara along with their detailed information.
It's based on two main endpoints:
 - `/employees/`
 - `/companies/`
 
These will provide you with paginated lists of given entities. You've also requested some more specific views.
Let me introduce to you how to use this tool.

In the first place you've requested to see:

    `Given a company, the API needs to return all their employees. 
    Provide the appropriate solution if the company does not have any employees.`

To serve this purpose I've designed a view of a company, that you can access via
 - `/companies/<name-of-company>`

For example: `/companies/PERMADYNE/` (this is not an advertisement, PERMADYNE company was selected randomly, I have no connections to it's management whatsoever)

Your second request was:

    `Given 2 people, provide their information (Name, Age, Address, phone) and the list of their friends 
    in common which have brown eyes and are still alive.
    
To serve this purpose I've designed a view of a company, that you can access via
 - `/employees/pair/?ids=<index-1>,<index-2>`

For example: `/employees/pair/?ids=1,2`. Index-1 and Index-2 are indexes assigned to every employee. If you want to check
what index is assigned to an employee, you can check by searching by his name like this:
 - `/employees/?username=Decker Mckenzie`
 
Your third request was:

    `Given 1 people, provide a list of fruits and vegetables they like. 
     This endpoint must respect this interface for the output:
     {"username": "Ahi", "age": "30", "fruits": ["banana", "apple"], "vegetables": ["beetroot", "lettuce"]}`
 
This is consumed by another endpoimt:

 - `/employees/<username>`

For example: `/employees/Decker%20Mckenzie/` (by the way, Decker proved himself as a great officer, he definitely deserves a raise)

# Chapter 3 - The Heist

```
    - paranuara (project root)
        |_ settings.py
        |_ tests.py
    - population (main application)
        |_ models.py
        |_ test
        |   |_ *tests*
        |
        |_ api
        |   |_ views.py
        |   |_ serializers.py
        |   |_ filters.py
        |
        |_ data_source
        |   |_ fetchers.py
        |   |_ parsers.py
        |   |_ mappings.py
        |
        |_ management
            |_ commands
                |_ populate_db.py
        
```

From the code perspective the application consists of a core `paranuara` project and `population` application. `population` 
consists tools for reading and parsing provided resources, defines db scheme, and whole API structure. Documents schemas
used for MongoDB are actually two models `Company` and `Employee`. They're filled with respective parsers from `data_source` that 
can easily be triggered with `python manage.py populate_db` command. API is based on DRF adapted to MongoDB schema which defines
filters, serializers and views. Application also has some tests that are run with help of custom TestRunner for MongoDB defined in 
`paranuara/tests.py` but tests weren't properly developed due to the quick delivery time of the whole project.

Another interesting features are `mongo_setup.js` file that acts as a initial script for db configuration.

# Epilogue

I hope that this instruction above has been clear enough Mr President. In case you needed any more information about this
fantastic project don't hesitate to contact me. Looking forward to other fascinating tasks, maybe something for the wild planet Pasablanco?
