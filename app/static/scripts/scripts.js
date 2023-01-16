$(document).ready(function () {
  $.ajaxSetup({ cache: false });

  function showResults(response) {
    // console.log(response);

    var outputHtml = "";

    if (response["type"] == 0) {
      outputHtml +=
        "<h4 class='center'> An exact match can't be found. Instead showing results for the closest word " +
        response["word"] +
        "</h4>";
    } else {
      outputHtml += "<h4> Search Results for " + response["word"] + "</h4>";
    }

    outputHtml += '<div class="list-group">';

    $.each(response["searchResults"], function (key, value) {
      outputHtml +=
        '<div class="list-group-item"><h4 class="list-group-item-heading">' +
        response["files"][key] +
        "</h4>";

      outputHtml += "<p>" + "Occurrend in the following lines" + "</p>";

      outputHtml +=
        '<p class="list-group-item">' + value["occurrence"] + "</p>" + "</div>";
    });

    outputHtml += "</div>";
    $("#searchUpdate").html(outputHtml);
  }

  function _noResult() {
    if ($(".list-group").is(":empty")) {
      $("#searchUpdate").html(
        '<div class="list-group"><div style="text-align:center" class="list-group-item"><h4 class="list-group-item-heading">No Result!</h4><p>Sorry, your search query returned no results. Help us make this tool better by clicking <a href="#0">here</a> to email the service desk with the term you would like to have added.</p></div></div>'
      );
    }
  }

  $("#searchButton").click(function () {
    let searchWord = $.trim($("#search").val());

    let origin = window.location.origin;

    jQuery.ajax({
      url: origin,
      type: "POST",
      data: JSON.stringify({ search: searchWord }),
      dataType: "json",
      contentType: "application/json",
      success: function (data) {
        let jsonData = $.parseJSON(data);

        if (Object.keys(jsonData["searchResults"]).length == 0) {
          _noResult();
        } else {
          showResults(jsonData);
        }
      },
    });

    setTimeout(_noResult, 1000);
  });

  // Clear search field and results
  $("#clearButton").click(function () {
    $("#search").val("");
    $("#nameOnly").prop("checked", false);
    $("#acronymOnly").prop("checked", false);
    // $('#searchUpdate').load('loader01.html');
    $("#searchUpdate").html("");
  });
});
