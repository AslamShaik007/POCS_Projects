const productive = document.querySelector("#productiveBtn");
const unProductive= document.querySelector("#unProductiveBtn");
const neutral = document.querySelector("#neutralBtn");

function productiveCall(evt) {
    const productiveAction = document.querySelector("#productiveBtn");
    if(productiveAction.checked) {
        var data = [trace1];
        var layout = {
            title: "US Export of Plastic Scrap",
            xaxis: {
                tickfont: {
                size: 14,
                color: "rgb(107, 107, 107)"
                }
            },
            yaxis: {
                title: "USD (millions)",
                titlefont: {
                size: 16,
                color: "rgb(107, 107, 107)"
                },
                tickfont: {
                size: 14,
                color: "rgb(107, 107, 107)"
                }
            },
            legend: {
                x: 0,
                y: 1.0,
                bgcolor: "rgba(255, 255, 255, 0)",
                bordercolor: "rgba(255, 255, 255, 0)"
            },
            barmode: "group",
            bargap: 0.15,
            bargroupgap: 0.1
        };
        Plotly.newPlot("myDiv", data, layout);
        // document.querySelector("#Productive").checked = true;
        document.querySelector("#unProductiveBtn").checked = false;
        document.querySelector("#neutralBtn").checked = false;
    } else {
        var data = [trace1, trace2, trace3];
        var layout = {
            title: "US Export of Plastic Scrap",
            xaxis: {
                tickfont: {
                size: 14,
                color: "rgb(107, 107, 107)"
                }
            },
            yaxis: {
                title: "USD (millions)",
                titlefont: {
                size: 16,
                color: "rgb(107, 107, 107)"
                },
                tickfont: {
                size: 14,
                color: "rgb(107, 107, 107)"
                }
            },
            legend: {
                x: 0,
                y: 1.0,
                bgcolor: "rgba(255, 255, 255, 0)",
                bordercolor: "rgba(255, 255, 255, 0)"
            },
            barmode: "group",
            bargap: 0.15,
            bargroupgap: 0.1
        };
        Plotly.newPlot("myDiv", data, layout);
        // document.querySelector("#Productive").checked = false;
        document.querySelector("#unProductiveBtn").checked = false;
        document.querySelector("#neutralBtn").checked = false;
    }

    
}

function UnproductiveCall(evt) {
    const unProductiveAction = document.querySelector("#unProductiveBtn");
    if(unProductiveAction.checked) {
        var data = [trace2];
        var layout = {
            title: "US Export of Plastic Scrap",
            xaxis: {
                tickfont: {
                size: 14,
                color: "rgb(107, 107, 107)"
                }
            },
            yaxis: {
                title: "USD (millions)",
                titlefont: {
                size: 16,
                color: "rgb(107, 107, 107)"
                },
                tickfont: {
                size: 14,
                color: "rgb(107, 107, 107)"
                }
            },
            legend: {
                x: 0,
                y: 1.0,
                bgcolor: "rgba(255, 255, 255, 0)",
                bordercolor: "rgba(255, 255, 255, 0)"
            },
            barmode: "group",
            bargap: 0.15,
            bargroupgap: 0.1
        };
        Plotly.newPlot("myDiv", data, layout);
         document.querySelector("#productiveBtn").checked = false;
        //  document.querySelector("#unProductiveBtn").checked = true;
         document.querySelector("#neutralBtn").checked = false;
    } else {
        var data = [trace1, trace2, trace3];
        var layout = {
            title: "US Export of Plastic Scrap",
            xaxis: {
                tickfont: {
                size: 14,
                color: "rgb(107, 107, 107)"
                }
            },
            yaxis: {
                title: "USD (millions)",
                titlefont: {
                size: 16,
                color: "rgb(107, 107, 107)"
                },
                tickfont: {
                size: 14,
                color: "rgb(107, 107, 107)"
                }
            },
            legend: {
                x: 0,
                y: 1.0,
                bgcolor: "rgba(255, 255, 255, 0)",
                bordercolor: "rgba(255, 255, 255, 0)"
            },
            barmode: "group",
            bargap: 0.15,
            bargroupgap: 0.1
        };
        Plotly.newPlot("myDiv", data, layout);
        document.querySelector("#productiveBtn").checked = false;
        //  document.querySelector("#unProductiveBtn").checked = false;
         document.querySelector("#neutralBtn").checked = false;
    }
    
}

function neutralCall(evt) {
    const neutralAction = document.querySelector("#neutralBtn");
    if(neutralAction.checked) {
        var data = [trace3];
        var layout = {
            title: "US Export of Plastic Scrap",
            xaxis: {
                tickfont: {
                size: 14,
                color: "rgb(107, 107, 107)"
                }
            },
            yaxis: {
                title: "USD (millions)",
                titlefont: {
                size: 16,
                color: "rgb(107, 107, 107)"
                },
                tickfont: {
                size: 14,
                color: "rgb(107, 107, 107)"
                }
            },
            legend: {
                x: 0,
                y: 1.0,
                bgcolor: "rgba(255, 255, 255, 0)",
                bordercolor: "rgba(255, 255, 255, 0)"
            },
            barmode: "group",
            bargap: 0.15,
            bargroupgap: 0.1
        };
        Plotly.newPlot("myDiv", data, layout);
        document.querySelector("#productiveBtn").checked = false;
         document.querySelector("#unProductiveBtn").checked = false;
        //  document.querySelector("#neutralBtn").checked = true;
    } else {
        document.querySelector("#productiveBtn").checked = false;
        document.querySelector("#unProductiveBtn").checked = false;
         document.querySelector("#neutralBtn").checked = false;
        var data = [trace1, trace2, trace3];
        var layout = {
            title: "US Export of Plastic Scrap",
            xaxis: {
                tickfont: {
                size: 14,
                color: "rgb(107, 107, 107)"
                }
            },
            yaxis: {
                title: "USD (millions)",
                titlefont: {
                size: 16,
                color: "rgb(107, 107, 107)"
                },
                tickfont: {
                size: 14,
                color: "rgb(107, 107, 107)"
                }
            },
            legend: {
                x: 0,
                y: 1.0,
                bgcolor: "rgba(255, 255, 255, 0)",
                bordercolor: "rgba(255, 255, 255, 0)"
            },
            barmode: "group",
            bargap: 0.15,
            bargroupgap: 0.1
        };
        Plotly.newPlot("myDiv", data, layout);
        
    }
    
}


var trace1 = {
    x: [ 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012 ],
    y: [ 219, 146, 112, 127, 124, 180, 236, 207, 236, 263, 350, 430, 474, 526, 488, 537, 500, 439 ],
    name: "Productive",
    marker: {
        // color: "rgb(55, 83, 109)"
        color: "rgb(103, 112, 220)"
    },
    type: "bar"
};

var trace2 = {
    x: [ 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012 ],
    y: [ 16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270, 299, 340, 403, 549, 499 ],
    name: "Unproductive",
    marker: {
        // color: "rgb(26, 118, 255)"
        color: "rgb(220, 103, 206)"
    },
    type: "bar"
};
    
var trace3 = {
    x: [ 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012 ],
    y: [ 16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270, 299, 340, 403, 549, 499 ],
    name: "Neutral",
    marker: {
        color: "rgb(103, 183, 220)"
    },
    type: "bar"
};

var data = [trace1, trace2, trace3];
var layout = {
    title: "US Export of Plastic Scrap",
    xaxis: {
        tickfont: {
        size: 14,
        color: "rgb(107, 107, 107)"
        }
    },
    yaxis: {
        title: "USD (millions)",
        titlefont: {
        size: 16,
        color: "rgb(107, 107, 107)"
        },
        tickfont: {
        size: 14,
        color: "rgb(107, 107, 107)"
        }
    },
    legend: {
        x: 0,
        y: 1.0,
        bgcolor: "rgba(255, 255, 255, 0)",
        bordercolor: "rgba(255, 255, 255, 0)"
    },
    barmode: "group",
    bargap: 0.15,
    bargroupgap: 0.1,
    options: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
    type: 'fitler'
};
Plotly.newPlot("myDiv", data, layout);