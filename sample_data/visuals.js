function getDateRange()
{
  	var output = document.getElementById("output");

    var inputDate = document.getElementById("date").value;
    output.innerHTML += inputDate + " is the date to search for.<br>";

    var funk=document.getElementById("enter");
    funk.addEventListener("click", getDateRange, false);

}
