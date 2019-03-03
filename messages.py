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