var Elements = (function () {
    var init_balanceAnalyticsChart = function () {
        var balanceAnalyticsChart = $('#balance-analytics-chart')

        var myBalanceAnalyticsChart = new Chart(balanceAnalyticsChart, {
            type: "line",
            data: {
                labels: [
                    "Janeiro",
                    "Fevereiro",
                    "Março",
                    "Abril",
                    "Maio",
                    "Junho",
                    "Julho",
                    "Agosto",
                    "Setembro",
                    "Otubro",
                    "Novembro",
                    "Dezembro",
                ],
                datasets: [
                    {
                        label: "Conta Corrente",
                        borderColor: "#1d7af3",
                        pointBorderColor: "#FFF",
                        pointBackgroundColor: "#1d7af3",
                        pointBorderWidth: 2,
                        pointHoverRadius: 4,
                        pointHoverBorderWidth: 1,
                        pointRadius: 4,
                        backgroundColor: "#1d7af3aa",
                        fill: true,
                        borderWidth: 2,
                        data: [4496.64, 4435.48, 1200.50, 2166.25, 3992.18, 1700.37, 4658.19, 2054.51, 1630.72, 4312.36, 1825.42, 1736.75],
                    },
                    {
                        label: "Conta Poupança",
                        borderColor: "#59d05d",
                        pointBorderColor: "#FFF",
                        pointBackgroundColor: "#59d05d",
                        pointBorderWidth: 2,
                        pointHoverRadius: 4,
                        pointHoverBorderWidth: 1,
                        pointRadius: 4,
                        backgroundColor: "#59d05daa",
                        fill: true,
                        borderWidth: 2,
                        data: [2503.11, 4928.53, 2708.89, 2757.87, 2583.02, 4227.21, 1640.30, 4832.69, 4644.53, 3932.44, 2417.31, 2230.17],
                    },
                    {
                        label: "Investimentos",
                        borderColor: "#f3545d",
                        pointBorderColor: "#FFF",
                        pointBackgroundColor: "#f3545d",
                        pointBorderWidth: 2,
                        pointHoverRadius: 4,
                        pointHoverBorderWidth: 1,
                        pointRadius: 4,
                        backgroundColor: "#f3545daa",
                        fill: true,
                        borderWidth: 2,
                        data: [2167.80, 1883.95, 2942.14, 4607.96, 4905.08, 2895.07, 3444.18, 3463.43, 1307.13, 4034.44, 3420.26, 4277.44],
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    position: "top",
                },
                tooltips: {
                    bodySpacing: 4,
                    mode: "nearest",
                    intersect: 0,
                    position: "nearest",
                    xPadding: 10,
                    yPadding: 10,
                    caretPadding: 10,
                },
                layout: {
                    padding: { left: 15, right: 15, top: 15, bottom: 15 },
                },
            },
        });
    }

    var init_cardsAnalyticsChart = function () {
        var cardsAnalyticsChart = $('#cards-analytics-chart')

        var myCardsAnalyticsChart = new Chart(cardsAnalyticsChart, {
            type: "bar",
            data: {
                labels: [
                    "Nubank",
                    "Itaú",
                ],
                datasets: [
                    {
                        label: "Limite",
                        backgroundColor: "rgb(23, 125, 255)",
                        borderColor: "rgb(23, 125, 255)",
                        data: [1500, 3600],
                    },
                    {
                        label: "Gastos",
                        backgroundColor: "rgb(255, 23, 11)",
                        borderColor: "rgb(255, 23, 11)",
                        data: [768.59, 1200.00],
                    },
                ],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    yAxes: [
                        {
                            ticks: {
                                beginAtZero: true,
                            },
                        },
                    ],
                },
            },
        });
    }

    var init_categoryChart = function () {
        var categoryChart = $('#category-chart')

        var myCategoryChart = new Chart(categoryChart, {
            type: "pie",
            data: {
                datasets: [
                    {
                        data: [50, 35, 15],
                        backgroundColor: ["#1d7af3", "#f3545d", "#fdaf4b"],
                        borderWidth: 0,
                    },
                ],
                labels: ["Lazer", "Alimentação", "Viagens"],
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    position: "bottom",
                    labels: {
                        fontColor: "rgb(154, 154, 154)",
                        fontSize: 11,
                        usePointStyle: true,
                        padding: 20,
                    },
                },
                pieceLabel: {
                    render: "percentage",
                    fontColor: "white",
                    fontSize: 14,
                },
                tooltips: false,
                layout: {
                    padding: {
                        left: 20,
                        right: 20,
                        top: 20,
                        bottom: 20,
                    },
                },
            },
        });

    }

    return {
        init: function () {
            init_balanceAnalyticsChart()
            init_cardsAnalyticsChart()
            init_categoryChart()
        }
    }
})()

jQuery(document).ready(function () {
    Elements.init()
})