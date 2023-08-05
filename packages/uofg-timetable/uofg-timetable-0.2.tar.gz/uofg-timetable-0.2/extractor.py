import requests
import time
import datetime
import pytz
import click
import itertools
import os
import pickle

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        show_timetable()

@cli.command()
@click.argument('guid')
@click.option('--password', prompt=True, hide_input=True)
def login(guid, password):
    """Login into UofG servers. 
    \n\n\nPS: The program doesn't store your username and password."""

    s = requests.Session()
    login_url = 'https://frontdoor.spa.gla.ac.uk/timetable/login'
    login_payload = {"guid": guid,"password": password,"rememberMe": False}
    r = s.post(login_url, json = login_payload)
    
    if r.status_code == 200:
        save_cookies(s)
        click.echo("Sucesfully logged in.")
        return s
    elif r.status_code == 403:
        raise click.ClickException("Invalid credentials, try again")
    else:
        raise click.ClickException(f'Something went wrong. The UofG servers responded with: \n Status code:  {r.status_code} \n Response Body: {r.json()}')
   
def save_cookies(session):
    '''
    Saves cookies from a session into a pickle dump named "cookies.p"
    '''
    with open( "cookies.p", "wb" ) as cookies_file:
        pickle.dump(session.cookies._cookies, cookies_file)

def retrieve_session():
    '''
    Starts a session and updates the cookies from a pickle dump named "cookies.p". 
    '''
    if not os.path.isfile("cookies.p") or os.stat('cookies.p').st_size == 0:
        invalid_credentials()

    click.echo("Retrieving session")
    s = requests.Session()
    with open( "cookies.p", "rb" ) as saved_cookies:
        cookies = pickle.load(saved_cookies)
        cj = requests.cookies.RequestsCookieJar()
        cj._cookies = cookies
        s.cookies = cj
    return s

def clear_screen():
    '''
    Run the clear screen command based on the user's OS.
    '''
    os.system('cls' if os.name=='nt' else 'clear')

def get_uk_timezone(date_time_str):
    '''
    Convert a Europe/london time in str to a datetime object.
    '''
    return pytz.timezone('Europe/London').localize(datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S'))

def get_datetime_obj(date_time_str):
    '''
    Convert a Europe/London timezone to user's timezone
    '''
    date_time_obj =  get_uk_timezone(date_time_str)
    return date_time_obj.astimezone(pytz.timezone('Asia/Kolkata')).time()

def get_timetable_json(startTime, endTime):
    '''
    Fetches timetable from UofG servers and refactors them for grouping with itertools.
    '''
    s = retrieve_session()
    
    click.echo("Fetching timetable from University of Glasgow...")
    
    timetable = s.get(f'https://frontdoor.spa.gla.ac.uk/timetable/timetable/events?start={startTime}&end={endTime}')

    if(timetable.status_code == 200):
        timetable = timetable.json()
        for slot in timetable:
            slot['date'] = get_uk_timezone(slot['start']).strftime('%d-%m-%Y (%A)')
        return timetable
    else:
        invalid_credentials()

@cli.command()
@click.option('--days', default=1, help="Number of days")
def show_timetable(days):
    '''
    Fetch your timetable from UofG. After which, display them in your local timezone.
    '''
    
    clear_screen()
    startTime = int(time.time())
    endTime = startTime + (86400 * days)
    timetable = get_timetable_json(startTime, endTime)
    timetable = itertools.groupby(timetable, lambda item: item["date"])
    
    clear_screen()
    click.echo(f'Timetable for the next {days} day(s)\n')
    for day in timetable:
        click.echo(f'On {day[0]} you have...\n')

        for count, slot in enumerate(day[1], 1):
            click.echo(f'{count}) {slot["course"]} from {get_datetime_obj(slot["start"])} to {get_datetime_obj(slot["end"])}')
        
        click.echo("-------------------------------\n")

def invalid_credentials():
    '''
    Raises an exception with a message about invalid credentials
    '''
    message = "You are no longer logged in or your credentials are not valid. \n\n"
    message += "Login using the command timetable login yourGUID"
    raise click.ClickException(message)

if __name__ == '__main__':
    cli()