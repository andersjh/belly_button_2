function buildMetadata(userData) {

  result = userData;
  console.log("result build meta\n", result);
  var PANEL = d3.select("#sample-metadata");
  PANEL.html("");

  // Use `Object.entries` to add each key and value pair to the panel
  // Hint: Inside the loop, you will need to use d3 to append new
  // tags for each key-value in the metadata.  
  Object.entries(result).forEach(([key, value]) => {
    PANEL.append("h6").text(`${key.toUpperCase()}: ${value}`);
  });  

  buildGauge(result.wfreq);

}

function buildCharts(sample) {
  
  var dataUrl = `/api/v1.0/info/${sample}`;

  var userInfo;
  d3.json(dataUrl).then((data) => {

    var resultArray = data.results;
    userInfo = data.user;

    var otu_ids = resultArray.map(info => info.otu_id);
    var otu_labels = resultArray.map(info => info.name);
    var sample_values = resultArray.map(info => info.amount);

    // Build a Bubble Chart
    var bubbleLayout = {
      title: "Bacteria Cultures Per Sample",
      margin: { t: 0 },
      hovermode: "closest",
      xaxis: { title: "OTU ID" },
      margin: { t: 30}
    };
    var bubbleData = [
      {
        x: otu_ids,
        y: sample_values,
        text: otu_labels,
        mode: "markers",
        marker: {
          size: sample_values,
          color: otu_ids,
          colorscale: "Earth"
        }
      }
    ];

    Plotly.newPlot("bubble", bubbleData, bubbleLayout);

    var yticks = otu_ids.slice(0, 10).map(otuID => `OTU ${otuID}`).reverse();
    var barData = [
      {
        y: yticks,
        x: sample_values.slice(0, 10).reverse(),
        text: otu_labels.slice(0, 10).reverse(),
        type: "bar",
        orientation: "h",
      }
    ];

    var barLayout = {
      title: "Top 10 Bacteria Cultures Found",
      margin: { t: 30, l: 150 }
    };

    Plotly.newPlot("bar", barData, barLayout);
    
    buildMetadata(userInfo);

  });

  

}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/api/v1.0/ids").then((data) => {
    var sampleNames = data;

    // Use the first sample from the list to build the initial plots
    var firstSample = sampleNames[0];
    var userData = buildCharts(firstSample);

  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  console.log(`change ${{newSample}}`)
  buildCharts(newSample);

}

// Initialize the dashboard
init();
