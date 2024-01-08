<template>
    <div class="card">
              <h2 class="title">Subject Grades</h2>

      <div class="card-shadow">

          <SubjectsChart />
      </div>
                    <h2 class="title" >Ethnic distribution</h2>

      <div class="card-shadow">
          <EthnicChart />
      </div>
    </div>

</template>

<script setup>
import { ref, onMounted } from "vue";
import SubjectsChart from "@/components/charts/SubjectsChart.vue";
import EthnicChart from "@/components/charts/EthnicChart.vue";
onMounted(async () => {
    const apiData = await fetchChartData();
    console.log(apiData)
    chartData.value = setChartData(apiData);
    chartOptions.value = setChartOptions();
});

const chartData = ref();
const chartOptions = ref();

// Function to fetch chart data from the API
const fetchChartData = async () => {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/line-scores'); // Adjust the URL as needed
      console.log(response)
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return await response.json();
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
    }
};

// Function to set chart data
// Function to set chart data
const setChartData = (apiData) => {
    const documentStyle = getComputedStyle(document.documentElement);

    // Convert the data dictionaries to arrays for the chart
    const datasets = apiData.datasets.map(dataset => {
        // Create an array for scores from 0 to 100
        const scoresArray = Array.from({ length: 101 }, (_, i) => i);

        // Map the scores array to the dataset format
        const data = scoresArray.map(score => ({
            x: score,
            y: dataset.data[score] || 0 // Use the score frequency or 0 if not present
        }));

        return {
            ...dataset,
            data,
            borderColor: documentStyle.getPropertyValue('--' + dataset.label.toLowerCase().replace(' ', '-') + '-500')
        };
    });

    return {
        labels: Array.from({ length: 101 }, (_, i) => i.toString()), // Labels from 0 to 100
        datasets
    };
};


// Function to set chart options
const setChartOptions = () => {
    const documentStyle = getComputedStyle(document.documentElement);
    const textColor = documentStyle.getPropertyValue('--text-color');
    const textColorSecondary = documentStyle.getPropertyValue('--text-color-secondary');
    const surfaceBorder = documentStyle.getPropertyValue('--surface-border');

    return {
        maintainAspectRatio: false,
        aspectRatio: 0.6,
        plugins: {
            legend: {
                labels: {
                    color: textColor
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    color: textColorSecondary
                },
                grid: {
                    color: surfaceBorder
                }
            },
            y: {
                ticks: {
                    color: textColorSecondary
                },
                grid: {
                    color: surfaceBorder
                }
            }
        }
    };
}
</script>

<style>
.card{
    display:flex;
  flex-direction:column;

}
.chart {

}

.card-shadow{
  width:60vw;
  height:auto;
  margin: 2rem auto;
  padding: 3rem;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  background-color: #fff;
}
.chart {
  height:60vh;
}

.title{
margin:5rem 0rem 1rem 0rem;
}

</style>
