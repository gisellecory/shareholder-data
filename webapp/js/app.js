// Script for dissertation, MSc Cardiff, September 2018

// Focus on search box
document.getElementById('search_term').focus();

///////////////////
// Initialise
// This function listens for user activation of the search
// It is executed on load of script
///////////////////

(function() {
  var search_button = document.getElementById('search_button');
  var search_box = document.getElementById('search_term');

  search_button.addEventListener('click', listener_search_button);
  search_button.addEventListener('keypress', listener_enter_press);
  search_box.addEventListener('keypress', listener_enter_press);
})();

///////////////////
// listener_enter_press
// This function defines the return/enter keyboard press for use in initialise function (above)
///////////////////

function listener_enter_press(e) {
  var key = e.which || e.keyCode;
  if (key === 13) {
    listener_search_button();
  }
}

////////////////////
// listener_search_button
// This function responds to a user's interaction with the search fields
///////////////////

var search_term;

function listener_search_button() {
  // Clear previous search results
  document.querySelector("#container_search_results").innerHTML = '';
  document.querySelector("#search_summary").innerHTML = '';

  // Get whatever is in search box
  search_term = document.getElementById('search_term').value.replace(/\s\s+/g, ' ').toLowerCase();
  // console.log(search_term)

  // If an empty search term was given
  if (search_term === "") {
    var alert_text = document.createTextNode("Please enter a search term");
    document.querySelector('#alert_searchterm_empty').appendChild(alert_text);
    return false;
  } else {

    // Set nonprofit based on filter selection
    // var is_nonprofit;
    //
    // if (document.getElementById('Choice_all').checked) {
    //   is_nonprofit = null;
    // } else if (document.getElementById('Choice_np').checked) {
    //   is_nonprofit = true;
    // } else if (document.getElementById('Choice_p').checked) {
    //   is_nonprofit = false;
    // }

    // var params = search_term;

    // var params = {
    //   search_term: search_term,
    //   // is_nonprofit: is_nonprofit,
    // };

    var res_sum_div = document.querySelector('#search_summary');
    var para_text = document.createTextNode("Searching...");
    var searching_para = document.createElement('p');
    searching_para.id = "searching_para";
    searching_para.appendChild(para_text);
    res_sum_div.appendChild(searching_para);

    getData(search_term);
  }
}

///////////////////
// getData
///////////////////

function getData(search_term) {

  // console.log(params)
  var _data;
  var search_results = [];
  var numb_results;
  // List for dictionaries
  var dict_list = [];

  d3.queue()
    // Get the text parser CSV
    .defer(d3.csv, "/data/sample_text_output.csv")
    .await(function(error, data) {

      // FOR EACH ROW IN CSV
      for (var i = 0; i < data.length; i++) {
        var names = data[i].Names;
        var names_lower = names.toLowerCase();

        // CLEAN UP DATA - THIS SHOULD BE DONE IN PYTHON SECTION
        // Remove apostrophes, remove [ ]
        // names = names.replace(/'/g, "");
        // names = names.replace(/]/g, "");
        // names = names.replace("[", "");

        // Split names string into a JS array
        var array = names.split(",");
        var array_lower = names_lower.split(",");

        // Set up regex
        var regex = "(\S+\s+)*" + search_term + "(\s+\S+)*";

        // Compare search input to elements of names array

        // FOR EACH NAME RETURNED FOR THAT METADATA ITEM
        for (var j = 0; j < array.length; j++) {

          array[j] = array[j].replace(/'/g, "");
          // if array[j] matches search_term, add array[j] to search_results list
          if (array_lower[j].match(regex) != null) {
            // Create empty dictionary (actually just a JS object)
            var dict = {};
            dict.ShName = array[j];
            if (data[i].category == "annual-return") {
              dict.Category = "an annual return"
            } else {
              dict.Category = "a conformation statement"
            }
            dict.CoNumb = data[i].co_numb;
            dict.Year = data[i].year;
            dict.Date = data[i].date;
            dict.CoName = data[i].CoName;
            dict.ChUri = data[i].ChUri;
            dict.Add1 = data[i].Add1;
            dict.Add2 = data[i].Add2;
            dict.Add3 = data[i].Add3;
            dict.Add4 = data[i].Add4;
            dict.AddCountry = data[i].AddCountry;
            dict.AddPC = data[i].AddPC;
            dict.CoCat = data[i].CoCat;
            dict.CountryOrigin = data[i].CountryOrigin;
            dict.Est = data[i].Est;
            dict.NextCS = data[i].NextCS;

            dict_list.push(dict);
            // console.log(dict);
          }
        }
      }
      numb_results = dict_list.length;
      // console.log(numb_results);

      // Search summary
      // Summary: No matches found for <search_term> OR One match found.... OR X matches found.....
      var res_sum_div = document.querySelector('#search_summary');
      res_sum_div.innerHTML = '';
      var para_sum = document.createElement('p');
      var match_text;
      if (numb_results > 1) {
        match_text = " matches for "
      } else {
        match_text = " match for "
      }
      var content_sum = numb_results + match_text + '"' + search_term + '"'
      var text_sum;
      if (numb_results > 0) {
        text_sum = document.createTextNode(content_sum);
        // text2 = document.createTextNode(temp2);
      } else {
        text_sum = document.createTextNode("No matches found for " + search_term);
      }
      para_sum.appendChild(text_sum);
      res_sum_div.appendChild(para_sum);

      // Search details
      // <sh_name> was listed as a shareholder of <co_name> in <sh_src_type> from <sh_src_year>. This company has company number <co_numb>. More details can be found at their Companies House webpage <ch_uri>.
      var results_div = document.querySelector('#container_search_results');
      results_div.innerHTML = '';
      var text_res;
      var para_res;
      var content_res;
      for (var k = 0; k < dict_list.length; k++) {

        // For each result
        content_res = dict_list[k].ShName + " was listed as a shareholder of " + dict_list[k].CoName + " in " + dict_list[k].Year
        text_res = document.createTextNode(content_res);
        para_res = document.createElement('p');
        var _div = document.createElement('div');

        para_res.appendChild(text_res);
        _div.appendChild(para_res);

        // Add list
        var list = document.createElement('ul');
        list.className = "co_list"

        // Registered company address:
        var _add = dict_list[k].Add1 + ", " + dict_list[k].Add2  + ", " + dict_list[k].Add3  + ", " + dict_list[k].Add4  + ", " + dict_list[k].AddCountry  + ", " + dict_list[k].AddPC;

        var list_content = [dict_list[k].CoNumb, _add, dict_list[k].CoCat, dict_list[k].Est, dict_list[k].CountryOrigin];

        var co_numb_text = "Company number: ";
        var add_text = "Registered company address: ";
        var co_type_text = "Co Type: "
        var est = "Established: "
        var origin = " Country of origin of company: "

        var list_text_labels = [co_numb_text, add_text, co_type_text, est, origin];

        for (var l = 0; l < list_content.length; l++) {
          var list_item = document.createElement('li');
          var list_text = document.createTextNode(list_text_labels[l] + list_content[l]);
          list_item.appendChild(list_text);
          list.appendChild(list_item);
        }

        var source_type = "Shareholder inforamtion found in "
        var source_date = " dated "
        var source_text = document.createTextNode(source_type + dict_list[k].Category + source_date + dict_list[k].Date + ". ");
        var source_para = document.createElement('p');
        source_para.appendChild(source_text);

        // Add link
        var para_link = document.createElement('p');
        var ch_link = "Go to filing details";
        var link = document.createElement('a');
        link.setAttribute("href", dict_list[k].ChUri);
        link.setAttribute("target", "_blank");
        link.append(ch_link);
        source_para.appendChild(link);

        var _break = document.createElement('hr');

        _div.appendChild(para_res);
        _div.appendChild(list);
        _div.appendChild(source_para);
        _div.appendChild(_break);
        results_div.appendChild(_div);


      }
    });
} // End of getData function
