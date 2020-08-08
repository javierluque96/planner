from django.shortcuts import render

from schedule.models import Event

# Create your views here.


def calc_percentage_done():
    try:
        events_done = Event.objects.filter(completed=True).count()
    except Event.DoesNotExist:
        events_done = 0
    total_events = Event.objects.all().count()

    if total_events != 0:
        return (events_done / total_events) * 100
    else:
        return 0


def add_event(title, start_time, end_time, day):
    added = False

    if end_time != 'End hour...':
        for hour in range(int(start_time), int(end_time)):
            print("%d" % (hour))
            if not Event.objects.filter(start_time=hour, day=day).exists():
                Event(title=title, start_time=hour, day=day).save()
                added = True
    else:
        if not Event.objects.filter(start_time=start_time, day=day).exists():
            Event(title=title, start_time=start_time, day=day).save()
            added = True

    return added


def find_event(day, hour):
    events = Event.objects.values()
    event = None
    for e in events:
        if e.get('start_time') == hour and e.get('day') == day:
            return e

    return event


def delete_event(id):
    try:
        Event.objects.get(id=int(id)).delete()
    except Event.DoesNotExist:
        pass


def modify_event(id, title, start_time, day, completed):
    try:
        if (not Event.objects.filter(start_time=start_time, day=day).exists()) or (find_event(day, start_time).get('id') == int(id)):
            Event.objects.filter(id=int(id)).update(
                title=title, start_time=start_time, day=day, completed=completed)
            return True
    except Event.DoesNotExist:
        return False


def display_events():
    days = ['monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday']
    display = ''

    for hour in range(24):
        # Displays the hours at the left
        display += '<div class="row"><div class="col-1 border text-center p-1">%s:00</div>' % hour

        for day in days:

            event = find_event(day, str(hour))

            if event is not None:
                title = event.get('title')
                id = event.get('id')
                day_options = ''
                hour_options = ''
                completed_html = '<input name="modify_completed" type="checkbox" class="form-check-input text-dark"'

                if event.get('completed'):
                    completed_html += 'checked'

                completed_html += '>'

                # generate the select for the forms --> day
                for d in days:
                    day_options += '<option '

                    if d == event.get('day'):
                        day_options += 'selected '

                    day_options += 'value="%s">%s</option>' % (
                        d, d.capitalize())

                # generate the select for the forms --> hour
                for h in range(24):
                    hour_options += '<option '

                    if h.__str__() == event.get('start_time'):
                        hour_options += 'selected '

                    hour_options += 'value="%s">%s:00</option>' % (
                        h, h)

                if event.get('completed'):
                    display += '<div class="schedule col border text-center p-1 bg-success">'

                else:
                    display += '<div class="schedule col border text-center p-1 bg-info">'

                display += '''
                    <button type = "button" style="border: none; background-color: inherit;" class="w-100 text-white" data-toggle="modal" data-target="#modal%s">
                        %s
                    </button>
                    <!-- Modal -->
                    <div class="modal fade" id="modal%s" tabindex="-1" role="dialog"" aria-hidden="true">
                        <div class="modal-dialog" role="document">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title">Modify event</h5>
                                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                                        <span aria-hidden="true">&times;</span>
                                    </button>
                                </div>

                                <div class="modal-body">
                                    <form class="form" action="/" method="GET">
                                        <input type="hidden" name="modify_event_id" value="%s">

                                        <div class="form-group mb-3">
                                            <input type="text" class="form-control" placeholder="Title" name="modify_title" value="%s">
                                        </div>

                                        <div class="form-group mb-3">
                                        <select class="form-control" name="modify_start_time">
                                            %s
                                        </select>
                                    </div>

                                    <div class="form-group mb-3">
                                        <select class="form-control" name="modify_day">
                                            %s
                                        </select>
                                    </div>
                                    <div class="form-check mb-3">
                                        %s
                                        <label class="form-check-label">
                                            Completed
                                        </label>
                                    </div>
                                        <div class="btn-group">
                                            <button type="text" class="btn btn-warning mr-1 rounded">Modify</button>
                                            
                                    </form> 

                                            <form class="form" action="/" method="GET">
                                                <input type="hidden" name="delete_event" value="%s">
                                                <button type="text" class="btn btn-danger ml-1 rounded">Delete</button>
                                            </form>
                                        </div>       
                                </div>   
                            </div>
                        </div>
                    </div>''' % (id, title, id, id, title, hour_options, day_options, completed_html, id)
                display += "</div>"

            else:
                display += '<div class="schedule col border text-center p-1"></div>'

        display += '</div>'

    return display


def schedule(request):
    error = None

    if request.POST.get("title"):
        if not add_event(request.POST["title"],
                    request.POST["start_time"], request.POST["end_time"], request.POST["day"]):
            error = "An event already exists at that time"

    if request.POST.get("reset_events"):
        Event.objects.all().delete()

    if request.GET.get("modify_event_id"):
        if (request.GET.get("modify_completed")):
            if not modify_event(request.GET["modify_event_id"], request.GET["modify_title"],
                         request.GET["modify_start_time"], request.GET["modify_day"], True):
                error = "An event already exists at that time"
        else:
            if not modify_event(request.GET["modify_event_id"], request.GET["modify_title"],
                         request.GET["modify_start_time"], request.GET["modify_day"], False):
                error = "An event already exists at that time"

    if request.GET.get("delete_event"):
        delete_event(request.GET.get("delete_event"))

    percentage_done = '{:3.2f}'.format(calc_percentage_done())

    return render(request, 'index.html', {"percentage_done": percentage_done, "events": display_events(), "range": range(24), "error": error})
