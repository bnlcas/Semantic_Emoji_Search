//Contains the basic script for the UI of a search bar
var entryField;
var inputDisplay;
var outputDisplay;

var search_term;

function start()
{
	entryField = document.getElementById("textInput");
	inputDisplay = document.getElementById("inputDisplay");
	outputDisplay = document.getElementById("outputDisplay");
	search_term = "";
	InitializeSearch();
}

$(document).ready(function () {
    $("#textInput").keydown(function(e) {
			keynum = e.keyCode;

			if(keynum == 13){
				SearchEmoji();
			}
		else {
			//Delete on Backspace
			if(keynum == 8 && search_term.length > 0)
			{
				search_term = search_term.slice(0,-1);
				//console.log(search_term);
			}
			else {
				search_term += String.fromCharCode(keynum).toLowerCase();
			}
		}
    });
});

function SearchEmoji()
{
	inputDisplay.innerHTML = "Search: " + search_term;
	outputDisplay.innerHTML = "Suggestions: ";
	entryField.value = "";
	var suggestions = FindEmoji(search_term);
	outputDisplay.innerHTML = "Suggestions: " + suggestions.reduce((acc, x) => acc + "  " +  x);
	search_term = "";
}
