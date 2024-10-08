const width = 800
const height = 600

const svg = d3
    .select("#graph")
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .call(
        d3.zoom().on("zoom", (event) => {
            svg.attr("transform", event.transform)
        })
    )
    .append("g")

const simulation = d3
    .forceSimulation()
    .force(
        "link",
        d3
            .forceLink()
            .id((d) => d.name)
            .distance(100)
    )
    .force("charge", d3.forceManyBody().strength(-300))
    .force("center", d3.forceCenter(width / 2, height / 2))

const color = d3.scaleOrdinal(d3.schemeCategory10)

function showLoading() {
    const loadingOverlay = document.getElementById("loading-overlay")
    if (loadingOverlay) {
        loadingOverlay.style.display = "flex"
    } else {
        console.warn("Loading overlay element not found")
    }
}

function hideLoading() {
    const loadingOverlay = document.getElementById("loading-overlay")
    if (loadingOverlay) {
        loadingOverlay.style.display = "none"
    } else {
        console.warn("Loading overlay element not found")
    }
}

function fetchData() {
    showLoading()
    return fetch("/api/v1/companies/")
        .then((response) => response.json())
        .then((companies) => {
            const nodes = companies
            const links = []

            const promises = companies.map((company) =>
                fetch(`/api/v1/companies/${company.name}/relationships/`)
                    .then((response) => response.json())
                    .then((relationships) => {
                        Object.entries(relationships).forEach(([type, related]) => {
                            related.forEach((relatedCompany) => {
                                links.push({
                                    source: company.name,
                                    target: relatedCompany.name,
                                    type: type,
                                })
                            })
                        })
                    })
            )

            return Promise.all(promises).then(() => {
                hideLoading()
                return { nodes, links }
            })
        })
        .then(({ nodes, links }) => {
            updateGraph(nodes, links)
        })
        .catch((error) => {
            console.error("Error fetching data:", error)
            hideLoading()
        })
}

function updateGraph(nodes, links) {
    const link = svg
        .selectAll(".link")
        .data(links)
        .join("line")
        .attr("class", "link")
        .attr("stroke", (d) => color(d.type))
        .attr("stroke-opacity", 0.6)
        .attr("stroke-width", 2)

    const node = svg
        .selectAll(".node")
        .data(nodes)
        .join("g")
        .attr("class", "node")
        .call(d3.drag().on("start", dragstarted).on("drag", dragged).on("end", dragended))

    node.append("circle")
        .attr("r", 10)
        .attr("fill", (d) => color(d.industry))

    node.append("text")
        .attr("dx", 12)
        .attr("dy", ".35em")
        .text((d) => d.name)
        .style("font-size", "12px")

    node.append("title").text(
        (d) => `${d.name}\nIndustry: ${d.industry}\nFounded: ${d.founded_year}`
    )

    simulation.nodes(nodes).on("tick", ticked)

    simulation.force("link").links(links)

    function ticked() {
        link.attr("x1", (d) => d.source.x)
            .attr("y1", (d) => d.source.y)
            .attr("x2", (d) => d.target.x)
            .attr("y2", (d) => d.target.y)

        node.attr("transform", (d) => `translate(${d.x},${d.y})`)
    }

    function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart()
        d.fx = d.x
        d.fy = d.y
    }

    function dragged(event, d) {
        d.fx = event.x
        d.fy = event.y
    }

    function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0)
        d.fx = null
        d.fy = null
    }
}

document.addEventListener("DOMContentLoaded", fetchData)
