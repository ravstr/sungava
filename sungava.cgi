#!/usr/bin/perl -w

use CGI qw/:standard/;
#use DBI;
##########################################################
#
# Real audio jukebox (perl)
##########################################################


print "Content-type:text/html\n\n";
require "mero.pl";

use Time::localtime;

read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
@pairs = split(/&/, $buffer);
foreach $pair (@pairs) {
   ($name, $value) = split(/=/, $pair);
   $value =~ tr/+/ /;
   $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;

   $value =~ s/\n/ /g;# added to strip line breaks 

   $FORM{$name} = $value;
}

$EXT = ".rpm";
$tm = localtime;
($DAY, $MONTH, $YEAR, $HR, $MIN, $SEC) = ($tm->mday, $tm->mon, $tm->year, $tm->hour, $tm->min, $tm->sec);

if($YEAR < 100)
{	$YEAR = $YEAR + 100;
}

# This remove the old .ram files on server

sub song_expire	
{
  local(@items, $item);
  opendir(RAMHANDLE, "./");
  @items = grep(/[0-9]$EXT/,readdir(RAMHANDLE));
  closedir(RAMHANDLE);
  foreach $item (@items)
   {
    ($YMD, $HMS) = split(/_/, $item);
  
	if($YMD != $YEAR.$MONTH.$DAY)
	{
		unlink("./$item");
	}
   }
}

&song_expire;

print <<EndHTML1;

          <html><head><title>::::--- Sungava.com ---::::</title>
          
 <SCRIPT LANGUAGE="JavaScript1.1">
<!-- Original:  Martin Webb (martinirt.org) -->

<!-- This script and many more are available free online at -->
<!-- The JavaScript Source!! http://javascript.internet.com -->

<!-- Begin
function right(e) {
if (navigator.appName == 'Netscape' && 
(e.which == 3 || e.which == 2))
return false;
else if (navigator.appName == 'Microsoft Internet Explorer' && 
(event.button == 2 || event.button == 3)) {
alert("Sorry, right click is disabled.");
return false;
}
return true;
}

document.onmousedown=right;
document.onmouseup=right;
if (document.layers) window.captureEvents(Event.MOUSEDOWN);
if (document.layers) window.captureEvents(Event.MOUSEUP);
window.onmousedown=right;
window.onmouseup=right;
//  End -->
</script>



         
	  		
<script language="Javascript">
	<!--
  		top.window.resizeTo(451, 250);
	//-->
	</script>
	<script language="Javascript" for="window" event="onresize()">
	<!--
  		document.body.scroll = 'no';
                document.body.status = 'no';
  		window.resizeTo(451, 250);
	//-->
	</script>


          </head>
          <body bgcolor="#999900" background="http://server33.hypermart.net/sungava/player.gif" link="#009999"><center>

EndHTML1

@Lists = split(/,/, $FORM{'text1'});


$FILE_NAME = $YEAR.$MONTH.$DAY. "_" .$HR.$MIN.$SEC.".rpm";
$FILE_NAME2 = ">".$FILE_NAME;
 
open(OUTF,$FILE_NAME2) or &dienice("Couldn't open survey.out for
         writing. Please notify webmaster.");

foreach $list (@Lists) {
	print OUTF "$Songs{$list}\n";
}

close(OUTF);

sub Redirect {
# Just in case the user's browser does not support redirections properly, we'll
# send out a document to tell them to go to the new location.  I have yet to
# see a browser that doesn't, but I figure it's better to be safe.
 print "<HTML><HEAD><TITLE>Note</TITLE>\n";

}


print <<EndHTML;
<SCRIPT LANGUAGE="JavaScript">
<!-- Real Jukebox JS Code Developed and Customized by Ravi Shrestha -->
<!-- 1999-2001 (c) -->
function DoNext(){ if (navigator.appName == 'Netscape') { document.sungava.DoNextItem(); } else { RAOCX.DoNextItem(); } } 

function DoPrev(){ if (navigator.appName == 'Netscape') { document.sungava.DoPrevItem();; } else { RAOCX.DoPrevItem();; } } 
function stop() { if (navigator.appName == 'Netscape') { document.sungava.DoStop(); } else { RAOCX.DoStop(); } } 
function play() { if (navigator.appName == 'Netscape') { document.sungava.DoPlay(); } else { RAOCX.DoPlay(); } } 
function inf() { if (navigator.appName == 'Netscape') { document.sungava.DoPause(); } else { RAOCX.DoPause(); } } 


</SCRIPT>

<object id="RAOCX" classid="clsid:CFCDAA03-8BE4-11cf-B84B-0020AFBBCCFA" width=280 height=100> 
<param name="controls" value="All">
<param name="autostart" value="true"> 
<param name="SRC" value="$FILE_NAME">        
<embed name="sungava" src="$FILE_NAME" controls="All" width="280" height="100" autostart="true" console="_master"> 
</object> 


 <p>

<table width="145" border="0" cellspacing="0" cellpadding="0" height="28">
          
		  <!-- Player Controls -->
		  
		     			<!-- RealPlayer -->
						  <tr> 
				            <td><img src="http://server33.hypermart.net/sungava/rewind.gif" width="32" height="28" alt="Previous song" onclick=DoPrev()></td>
				            <td><img src="http://server33.hypermart.net/sungava/play.gif" width="32" height="28" alt="Play" onmousedown=play()></td>
				            <td><img src="http://server33.hypermart.net/sungava/stop.gif" width="34" height="28" alt="Stop" onmousedown=stop()></td>
				            <td><img src="http://server33.hypermart.net/sungava/ffwd.gif" width="32" height="28" alt="Next song" onmousedown=DoNext()></td>
                                            <td><img src="http://server33.hypermart.net/sungava/player.gif" width="34" height="28"></td>

				          </tr>
							
		  <!-- end player controls -->
        </table>
        <br><font size-"-1" color="white">
	<center>
</center></font>
<img src="http://server33.hypermart.net/sungava/counter/logcnt.cgi?t" valign="middle" width="1" height="1">
        
EndHTML
          

print	"</body></html>";

          sub dienice {
              ($msg) = @_;
              print "<h2>Error</h2>\n";
              print $msg;
              exit;
}
