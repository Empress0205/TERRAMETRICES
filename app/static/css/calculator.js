// Emission Factors (example values)
const emissionFactors = {
    electricity: 0.92, // kg CO₂ per kWh
    naturalGas: 5.3,   // kg CO₂ per therm
    heatingFuel: 10.1, // kg CO₂ per gallon
    carMileage: 0.404, // kg CO₂ per mile
    publicTransport: 0.1, // kg CO₂ per hour
    airTravel: 0.254,  // kg CO₂ per mile
    diet: {
        vegetarian: 1.5, // tons CO₂/year
        vegan: 1.0,
        meatHeavy: 2.5,
    },
    waste: {
        low: 0.5, // tons CO₂/year
        medium: 1.0,
        high: 1.5,
    },
};

// Category Selection
document.getElementById('category').addEventListener('change', function () {
    const category = this.value;
    const inputFields = document.getElementById('input-fields');
    inputFields.innerHTML = getInputFields(category);
});

// Get Input Fields Based on Category
function getInputFields(category) {
    if (category === 'personal') {
        return `
            <h2>Energy Usage</h2>
            <label for="electricity">Electricity Consumption (kWh/month):</label>
            <input type="number" id="electricity" placeholder="Enter kWh">

            <label for="natural-gas">Natural Gas Usage (therms/month):</label>
            <input type="number" id="natural-gas" placeholder="Enter therms">

            <label for="heating-fuel">Heating Fuel Usage (gallons/month):</label>
            <input type="number" id="heating-fuel" placeholder="Enter gallons">

            <h2>Transportation</h2>
            <label for="car-mileage">Car Mileage (miles/year):</label>
            <input type="number" id="car-mileage" placeholder="Enter miles">

            <label for="public-transport">Public Transport Usage (hours/week):</label>
            <input type="number" id="public-transport" placeholder="Enter hours">

            <label for="air-travel">Air Travel (flights/year):</label>
            <input type="number" id="air-travel" placeholder="Enter flights">

            <h2>Lifestyle</h2>
            <label for="diet">Diet:</label>
            <select id="diet">
                <option value="vegetarian">Vegetarian</option>
                <option value="vegan">Vegan</option>
                <option value="meatHeavy">Meat-Heavy</option>
            </select>

            <label for="waste">Waste Production:</label>
            <select id="waste">
                <option value="low">Low (Recycles regularly)</option>
                <option value="medium">Medium (Some recycling)</option>
                <option value="high">High (Mostly landfill)</option>
            </select>
        `;
    } else if (category === 'organization') {
        return `
            <h2>Energy Usage</h2>
            <label for="electricity">Electricity Consumption (kWh/month):</label>
            <input type="number" id="electricity" placeholder="Enter kWh">

            <label for="natural-gas">Natural Gas Usage (therms/month):</label>
            <input type="number" id="natural-gas" placeholder="Enter therms">

            <label for="heating-fuel">Heating Fuel Usage (gallons/month):</label>
            <input type="number" id="heating-fuel" placeholder="Enter gallons">

            <h2>Transportation</h2>
            <label for="fleet-mileage">Fleet Mileage (miles/year):</label>
            <input type="number" id="fleet-mileage" placeholder="Enter miles">

            <label for="employee-commuting">Employee Commuting (miles/year):</label>
            <input type="number" id="employee-commuting" placeholder="Enter miles">

            <h2>Operations</h2>
            <label for="waste">Waste Production:</label>
            <select id="waste">
                <option value="low">Low (Recycles regularly)</option>
                <option value="medium">Medium (Some recycling)</option>
                <option value="high">High (Mostly landfill)</option>
            </select>
        `;
    } else if (category === 'country') {
        return `
            <h2>Energy Production</h2>
            <label for="electricity">Electricity Consumption (kWh/year):</label>
            <input type="number" id="electricity" placeholder="Enter kWh">

            <label for="natural-gas">Natural Gas Usage (therms/year):</label>
            <input type="number" id="natural-gas" placeholder="Enter therms">

            <h2>Transportation</h2>
            <label for="vehicle-miles">Vehicle Miles Traveled (miles/year):</label>
            <input type="number" id="vehicle-miles" placeholder="Enter miles">

            <label for="public-transport">Public Transport Usage (hours/year):</label>
            <input type="number" id="public-transport" placeholder="Enter hours">
        `;
    }
    return '';
}

// Calculate Button Event Listener
document.getElementById('calculate-button').addEventListener('click', calculateFootprint);

function calculateFootprint() {
    const category = document.getElementById('category').value;
    let totalEmissions = 0;

    if (category === 'personal') {
        const electricity = parseFloat(document.getElementById('electricity').value) || 0;
        const naturalGas = parseFloat(document.getElementById('natural-gas').value) || 0;
        const heatingFuel = parseFloat(document.getElementById('heating-fuel').value) || 0;
        const carMileage = parseFloat(document.getElementById('car-mileage').value) || 0;
        const publicTransport = parseFloat(document.getElementById('public-transport').value) || 0;
        const airTravel = parseFloat(document.getElementById('air-travel').value) || 0;
        const diet = document.getElementById('diet').value;
        const waste = document.getElementById('waste').value;

        totalEmissions = (electricity * emissionFactors.electricity) +
                         (naturalGas * emissionFactors.naturalGas) +
                         (heatingFuel * emissionFactors.heatingFuel) +
                         (carMileage * emissionFactors.carMileage) +
                         (publicTransport * emissionFactors.publicTransport) +
                         (airTravel * emissionFactors.airTravel) +
                         (emissionFactors.diet[diet] * 1000) + // Convert tons to kg
                         (emissionFactors.waste[waste] * 1000); // Convert tons to kg
    } else if (category === 'organization') {
        const electricity = parseFloat(document.getElementById('electricity').value) || 0;
        const naturalGas = parseFloat(document.getElementById('natural-gas').value) || 0;
        const heatingFuel = parseFloat(document.getElementById('heating-fuel').value) || 0;
        const fleetMileage = parseFloat(document.getElementById('fleet-mileage').value) || 0;
        const employeeCommuting = parseFloat(document.getElementById('employee-commuting').value) || 0;
        const waste = document.getElementById('waste').value;

        totalEmissions = (electricity * emissionFactors.electricity) +
                         (naturalGas * emissionFactors.naturalGas) +
                         (heatingFuel * emissionFactors.heatingFuel) +
                         (fleetMileage * emissionFactors.carMileage) +
                         (employeeCommuting * emissionFactors.carMileage) +
                         (emissionFactors.waste[waste] * 1000); // Convert tons to kg
    } else if (category === 'country') {
        const electricity = parseFloat(document.getElementById('electricity').value) || 0;
        const naturalGas = parseFloat(document.getElementById('natural-gas').value) || 0;
        const vehicleMiles = parseFloat(document.getElementById('vehicle-miles').value) || 0;
        const publicTransport = parseFloat(document.getElementById('public-transport').value) || 0;

        totalEmissions = (electricity * emissionFactors.electricity) +
                         (naturalGas * emissionFactors.naturalGas) +
                         (vehicleMiles * emissionFactors.carMileage) +
                         (publicTransport * emissionFactors.publicTransport);
    }

    // Convert kg to tons
    totalEmissions = totalEmissions / 1000;

    // Display Results
    document.getElementById('total-emissions').textContent = totalEmissions.toFixed(2);

    // Display Recommendations
    const recommendations = [
        "Switch to renewable energy sources.",
        "Use public transportation or carpool.",
        "Reduce air travel and opt for virtual meetings.",
        "Adopt a plant-based diet.",
        "Recycle and reduce waste production.",
    ];
    const recommendationsList = document.getElementById('recommendations');
    recommendationsList.innerHTML = recommendations.map(rec => `<li>${rec}</li>`).join('');
}