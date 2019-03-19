from types import SimpleNamespace

club={
    'details':'Club details successfully send.',
    'member':'Member list send',
    'amfailure':'Either User is not registered in app or you have not permission to add members',
    'amalready':'Member already exist in club',
    'amsuccess':'member added successfully',
    'rmfailure':'This is only for admins of club',
    'rmsuccess':'member deleted succesfully',
    'fcsuccess':'You have started following club.',
    'ucsuccess':'You have just unfollowed club.',
    'not_exist':'User is not Registered in app',
}
clubs=SimpleNamespace(**club)

user={
    'wsucess':'Welcome to the app',
    'rsuccess':'Email verification has been sent to your email.',
    'rfailure':'User already Exist',
    'vsuccess':'OTP verified',
    'vfailure':'OTP not verified',
    'lfailure':'Invalid credentials',
    'lsuccess':'Logged in Successfully',
    'fpfailure':'This user is not registered in app',
    'fpsuccess':'Resest password has been sent to registered email',
    'rpsuccess':'Password Changed Successfully',
    'rpfailure':'OTP not verified',


}
users=SimpleNamespace(**user)

event={
    'ecsuccess':'Event has been created successfully.',
    'list':'Event List sent.',
    'details':'Event Details successfully sent',
    'delete':'Event has been deleted.',
    'club_event_list':'Event of this club is sent.'
}
events=SimpleNamespace(**event)

new={
    'nsuccess':'News has been posted successfully',
    'delete':'News has been deleted'

}
news=SimpleNamespace(**new)