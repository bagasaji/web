$(document).ready(function () {
    function fetchData() {
        $.get('/data', function (data) {
            console.log(data); // Check data received in browser console
            if (data.message) {
                $('#dataContainer').append('<div class="alert alert-danger" role="alert">' + data.message + '</div>');
            } else {
                $('#dataContainer').empty(); // Clear container before adding new data
                
                // Loop through each item in the data array
                data.forEach(function(item) {
                    $('#dataContainer').append('<div class="col-xl-3 col-md-6 mb-4">' +
                        '<div class="card border-left-primary shadow h-100 py-2">' +
                        '<div class="card-body p-2">' +
                        '<div class="row no-gutters align-items-center">' +
                        '<div class="col mr-2">' +
                        '<div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Nitrogen</div>' +
                        '<div id="nitrogen" class="h5 mb-0 font-weight-bold text-gray-800">' + item.Nitrogen + '</div>' +
                        '</div></div></div></div></div>');
                    
                    $('#dataContainer').append('<div class="col-xl-3 col-md-6 mb-4">' +
                        '<div class="card border-left-success shadow h-100 py-2">' +
                        '<div class="card-body p-2">' +
                        '<div class="row no-gutters align-items-center">' +
                        '<div class="col mr-2">' +
                        '<div class="text-xs font-weight-bold text-success text-uppercase mb-1">Phosphor</div>' +
                        '<div id="phosphor" class="h5 mb-0 font-weight-bold text-gray-800">' + item.Phosphor + '</div>' +
                        '</div></div></div></div></div>');
                    
                    $('#dataContainer').append('<div class="col-xl-3 col-md-6 mb-4">' +
                        '<div class="card border-left-info shadow h-100 py-2">' +
                        '<div class="card-body p-2">' +
                        '<div class="row no-gutters align-items-center">' +
                        '<div class="col mr-2">' +
                        '<div class="text-xs font-weight-bold text-info text-uppercase mb-1">Kalium</div>' +
                        '<div id="potassium" class="h5 mb-0 font-weight-bold text-gray-800">' + item.Kalium + '</div>' +
                        '</div></div></div></div></div>');
                    
                    $('#dataContainer').append('<div class="col-xl-3 col-md-6 mb-4">' +
                        '<div class="card border-left-warning shadow h-100 py-2">' +
                        '<div class="card-body p-2">' +
                        '<div class="row no-gutters align-items-center">' +
                        '<div class="col mr-2">' +
                        '<div class="text-xs font-weight-bold text-warning text-uppercase mb-1">Temperature</div>' +
                        '<div id="temperature" class="h5 mb-0 font-weight-bold text-gray-800">' + item.Temperature + '</div>' +
                        '</div></div></div></div></div>');
                    
                    $('#dataContainer').append('<div class="col-xl-3 col-md-6 mb-4">' +
                        '<div class="card border-left-danger shadow h-100 py-2">' +
                        '<div class="card-body p-2">' +
                        '<div class="row no-gutters align-items-center">' +
                        '<div class="col mr-2">' +
                        '<div class="text-xs font-weight-bold text-danger text-uppercase mb-1">Moisture</div>' +
                        '<div id="moisture" class="h5 mb-0 font-weight-bold text-gray-800">' + item.Humidity + '</div>' +
                        '</div></div></div></div></div>');
                    
                    $('#dataContainer').append('<div class="col-xl-3 col-md-6 mb-4">' +
                        '<div class="card border-left-secondary shadow h-100 py-2">' +
                        '<div class="card-body p-2">' +
                        '<div class="row no-gutters align-items-center">' +
                        '<div class="col mr-2">' +
                        '<div class="text-xs font-weight-bold text-secondary text-uppercase mb-1">pH</div>' +
                        '<div id="ph" class="h5 mb-0 font-weight-bold text-gray-800">' + item.ph + '</div>' +
                        '</div></div></div></div></div>');
                    
                    $('#dataContainer').append('<div class="col-xl-3 col-md-6 mb-4">' +
                        '<div class="card border-left-dark shadow h-100 py-2">' +
                        '<div class="card-body p-2">' +
                        '<div class="row no-gutters align-items-center">' +
                        '<div class="col mr-2">' +
                        '<div class="text-xs font-weight-bold text-dark text-uppercase mb-1">Conductivity</div>' +
                        '<div id="conductivity" class="h5 mb-0 font-weight-bold text-gray-800">' + item.Conductivity + '</div>' +
                        '</div></div></div></div></div>');
                    
                    // Add additional card code here as needed
                });
            }
        });
    }

    fetchData(); // Call fetchData function when document is ready

    $('#trainModel').click(function () {
        $.get('/train', function (response) {
            $('#predictionResult').html('<div class="alert alert-success" role="alert">Model trained successfully! Accuracy: ' + response.accuracy + '</div>');
        }).fail(function () {
            $('#predictionResult').html('<div class="alert alert-danger" role="alert">Failed to train model!</div>');
        });
    });

    $('#getPrediction').click(function () {
        $.get('/predict', function (response) {
            $('#predictionResult').html('<div class="alert alert-info" role="alert">Prediction: ' + response.prediction + '</div>');
        }).fail(function () {
            $('#predictionResult').html('<div class="alert alert-danger" role="alert">Failed to get prediction!</div>');
        });
    });
});
