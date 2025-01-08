<template>
  <div v-if="load" class="analytics-container">
    <div class="row border border-dark container bg-light">
      <div class="chart border border-dark w-100">
        <canvas id="bookIssuedChart"></canvas>
      </div>
    </div>

    <div class="chart border border-dark">
      <canvas id="genreDistributionChart"></canvas>
    </div>

    <div class="chart">
      <canvas id="topSellingBooksChart"></canvas>
    </div>

    <div class="chart">
      <canvas id="popularBooksChart"></canvas>
    </div>
  </div>
  <div v-else class="fluid-container h-100 bg-secondary p-3 m-2">
    <h1>loading...</h1>
  </div>
</template>

<script>
export default {
  name: 'AnalyticsDashboard',
  data() {
    return {
      load: false,
      bookIssuedData: { books_issued: [], date: [] },
      genreDistributionData: { section: [], count: [] },
      topSellingBooksData: [],
      popularBooksData: [],
    };
  },
  methods: {
  async fetchData() {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/analytics', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${sessionStorage.getItem('jwt_token')}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        this.bookIssuedData = data.book_issued_data;
        this.genreDistributionData = data.genre_distribution;
        this.topSellingBooksData = data.top_selling_books;
        this.popularBooksData = data.popular_book;
        this.load = true;
        this.$nextTick(() => {
          this.renderCharts();
        });
      } else {
        console.error('Failed to fetch analytics data');
      }
    } catch (error) {
      console.error('Error fetching analytics data:', error);
    }
  },
  renderCharts() {
    const Chart = window.Chart;

    // Book Issued Line Chart
    new Chart(document.getElementById('bookIssuedChart').getContext('2d'), {
      type: 'line',
      data: {
        labels: this.bookIssuedData.date,
        datasets: [{
          label: 'Books Issued Per Day',
          data: this.bookIssuedData.books_issued,
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
          fill: false,
        }],
      },
      options: {
        scales: {
          x: {
            title: {
              display: true,
              text: 'Date',
            },
            ticks: {
              autoSkip: true,
              maxTicksLimit: 10,
            },
          },
          y: {
            title: {
              display: true,
              text: 'Number of Books Issued',
            },
            beginAtZero: true,
          },
        },
      },
    });

    // Genre Distribution Pie Chart
    new Chart(document.getElementById('genreDistributionChart').getContext('2d'), {
      type: 'pie',
      data: {
        labels: this.genreDistributionData.section,
        datasets: [{
          label: 'Genre Distribution',
          data: this.genreDistributionData.count,
          backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
        }],
      },
    });

    // Top Selling Books Bar Chart
    new Chart(document.getElementById('topSellingBooksChart').getContext('2d'), {
      type: 'bar',
      data: {
        labels: this.topSellingBooksData.map(item => item[0]),
        datasets: [{
          label: 'Top Selling Books',
          data: this.topSellingBooksData.map(item => item[1]),
          backgroundColor: 'rgba(153, 102, 255, 0.2)',
          borderColor: 'rgba(153, 102, 255, 1)',
          borderWidth: 1,
        }],
      },
      options: {
        scales: {
          x: {
            title: {
              display: true,
              text: 'Book Title',
            },
            ticks: {
              autoSkip: true,
              maxTicksLimit: 10,
            },
          },
          y: {
            title: {
              display: true,
              text: 'Number of Copies Sold',
            },
            beginAtZero: true,
          },
        },
      },
    });
    

    // Popular Books Bar Chart
    new Chart(document.getElementById('popularBooksChart').getContext('2d'), {
      type: 'bar',
      data: {
        labels: this.popularBooksData.map(item => item[0]),
        datasets: [{
          label: 'Most Rated Books',
          data: this.popularBooksData.map(item => item[1]),
          backgroundColor: 'rgba(153, 102, 255, 0.2)',
          borderColor: 'rgba(153, 102, 255, 1)',
          borderWidth: 1,
        }],
      },
      options: {
        scales: {
          x: {
            title: {
              display: true,
              text: 'Book Title',
            },
            ticks: {
              autoSkip: true,
              maxTicksLimit: 5,
            },
          },
          y: {
            title: {
              display: true,
              text: 'Rating ',
            },
            beginAtZero: true,
          },
        },
      },
    });
  
  },
},

  mounted() {
    this.fetchData();
  },
};
</script>

<style scoped>
.analytics-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  gap: 2rem;
}

.chart {
  width: 45%;
  min-width: 300px;
  margin-bottom: 1rem;
}
</style>
