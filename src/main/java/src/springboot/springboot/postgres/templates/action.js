function deleteAccount() {
    if (window.confirm("Are you sure you want to delete your account?")) { 
        window.location.replace("http://127.0.0.1:8001/bank/Lewis/delete/");
      } else{
        window.location.replace("http://127.0.0.1:8001/bank/Lewis/settings/");
      }
        document.getElementById("demo").innerHTML;
    }

    function logout() {
        if (window.confirm("Are you sure you want to sign out?")) { 
            window.location.replace("http://127.0.0.1:8001/bank/Lewis/logout/");
          } else{
            window.location.replace("http://127.0.0.1:8001/bank/Lewis/settings/");
          }
            document.getElementById("demo").innerHTML;
        }