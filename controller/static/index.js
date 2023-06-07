function updateTemperatureOutput() {
  var outputElement = $("#output_temperature");

  outputElement.removeClass("zoom-effect");

  $.ajax({
    url: "/temperature",
    success: function (data) {
      outputElement.text(data);

      if (data.includes("SUSPENDED")) {
        $(".grid-item h1:contains('" + "temperature".toUpperCase() + "')")
          .closest(".grid-item")
          .css("background-color", "#843131");
      } else {
        $(".grid-item h1:contains('" + "temperature".toUpperCase() + "')")
          .closest(".grid-item")
          .css("background-color", "#3e3e3e");
      }

      outputElement.addClass("zoom-effect");
    },
  });
}

function updateWeightOutput() {
  var outputElement = $("#output_weight");

  outputElement.removeClass("zoom-effect");

  $.ajax({
    url: "/weight",
    success: function (data) {
      outputElement.text(data);

      if (data.includes("SUSPENDED")) {
        $(".grid-item h1:contains('" + "weight".toUpperCase() + "')")
          .closest(".grid-item")
          .css("background-color", "#843131");
      } else {
        $(".grid-item h1:contains('" + "weight".toUpperCase() + "')")
          .closest(".grid-item")
          .css("background-color", "#3e3e3e");
      }

      outputElement.addClass("zoom-effect");
    },
  });
}

function updateLedOutput() {
  var outputElement = $("#output_led");

  outputElement.removeClass("zoom-effect");

  $.ajax({
    url: "/led",
    success: function (data) {
      outputElement.text(data);

      if (data.includes("SUSPENDED")) {
        $(".grid-item h1:contains('" + "led".toUpperCase() + "')")
          .closest(".grid-item")
          .css("background-color", "#843131");
      } else {
        $(".grid-item h1:contains('" + "led".toUpperCase() + "')")
          .closest(".grid-item")
          .css("background-color", "#3e3e3e");
      }

      outputElement.addClass("zoom-effect");
    },
  });
}

function updateHeaterOutput() {
  var outputElement = $("#output_heater");

  outputElement.removeClass("zoom-effect");

  $.ajax({
    url: "/heater",
    success: function (data) {
      outputElement.text(data);

      if (data.includes("SUSPENDED")) {
        $(".grid-item h1:contains('" + "heater".toUpperCase() + "')")
          .closest(".grid-item")
          .css("background-color", "#843131");
      } else {
        $(".grid-item h1:contains('" + "heater".toUpperCase() + "')")
          .closest(".grid-item")
          .css("background-color", "#3e3e3e");
      }

      outputElement.addClass("zoom-effect");
    },
  });
}

function chooseCoaster(selectedValue) {
  $.ajax({
    url: "/topics",
    method: "POST",
    data: { selectedValue: selectedValue },
    success: function (response) {
      console.log("Request sent successfully!");
    },
    error: function (xhr, status, error) {
      console.log("Error sending request:", error);
    },
  });
}

function handleGridItemClick(item) {
  var selectedTopic = $("#topic").val();
  var topicSuffix = selectedTopic.trim().slice(1);
  $.ajax({
    url: "/" + item,
    method: "POST",
    data: { item: (item += topicSuffix) },
    success: function (response) {
      console.log("Request sent successfully!");
    },
    error: function (xhr, status, error) {
      console.log("Error sending request:", error);
    },
  });
}

$(document).ready(function () {
  updateTemperatureOutput();
  updateWeightOutput();
  updateLedOutput();
  updateHeaterOutput();
  setInterval(updateTemperatureOutput, 2000);
  setInterval(updateWeightOutput, 2000);
  setInterval(updateLedOutput, 2000);
  setInterval(updateHeaterOutput, 2000);

  $(".grid-item").on("click", function () {
    var itemId = $(this).find("h1").text().trim().toLowerCase();
    handleGridItemClick(itemId);
  });

  $("#topic").on("change", function () {
    var selectedValue = $(this).val();
    chooseCoaster(selectedValue);
  });
});
