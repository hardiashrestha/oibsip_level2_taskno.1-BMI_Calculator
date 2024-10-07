document.getElementById('calculateBtn').addEventListener('click', function() {
    const weight = document.getElementById('weight').value;
    const height = document.getElementById('height').value;

    fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `weight=${weight}&height=${height}`
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result').innerHTML = `BMI: ${data.bmi}, Category: ${data.category}`;
        document.getElementById('result').style.animation = "fadeIn 1s";
    })
});