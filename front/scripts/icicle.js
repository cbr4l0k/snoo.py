const DK_BG =        '#282828';
const DK_RED =       '#cc241d';
const DK_GREEN =     '#98971a';
const DK_YELLOW =    '#d79921';
const DK_BLUE =      '#458588';
const DK_PURPLE =    '#b16286';
const DK_AQUA =      '#689d6a';
const DK_GRAY =      '#928374';
const DK_ORANGE =    '#d65d0e';
const LG_BG =        '#ebdbb22'
const LG_RED =       '#fb4934';
const LG_GREEN =     '#b8bb26';
const LG_YELLOW =    '#fabd2f';
const LG_BLUE =      '#83a598';
const LG_PURPLE =    '#d3869b';
const LG_AQUA =      '#8ec07c';
const LG_GRAY =      '#a89984';
const LG_ORANGE =    '#fe8019';

/**
 * Function to draw a icicle chart.
 * @param {Object} data - The data to be used for the chart.
 */
function draw_icicle(data) {
    // Specify the chart’s dimensions.
    const width = 650;
    const height = window.screen.availHeight * 0.75;
    console.log()

    // Create the color scale.
    const color = d3.scaleOrdinal(d3.quantize(d3.interpolate(LG_YELLOW, LG_GREEN), data.children.length + 1));

    // Compute the layout.
    const hierarchy = d3.hierarchy(data)
        .sum(d => {return d.times_called;})
        .sort((a, b) => b.height - a.height || b.times_called - a.times_called);
    const root = d3.partition()
        .size([height, (hierarchy.height + 1) * width / 3])
    (hierarchy);

    // Create the SVG container.
    const svg = d3.select("svg#svg_sb")
        .attr("viewBox", [0, 0, width, height])
        .attr("width", width)
        .attr("height", height)
        .attr("style", "max-width: 100%;" +
                        "height: auto;" +
                        "font: 4px;" +
                        "border-radius: 5px;" + 
                        "font-family: 'Courier New', monospace;"
        );

    // Append cells.
    const cell = svg
        .selectAll("g")
        .data(root.descendants())
        .join("g")
        .attr("transform", d => `translate(${d.y0},${d.x0})`);

    const rect = cell.append("rect")
        .attr("width", d => d.y1 - d.y0 - 1)
        .attr("height", d => rectHeight(d))
        .attr("fill-opacity", 0.6)
        .attr("fill", d => {
            if (!d.depth) return DK_YELLOW;
            while (d.depth > 1) d = d.parent;
            return color(d.data.name);
        })
        .style("cursor", "pointer")
        .on("click", clicked);

    const text = cell.append("text")
        .style("user-select", "none")
        .attr("pointer-events", "none")
        .attr("x", 4)
        .attr("y", 13)
        .attr("fill-opacity", d => +labelVisible(d));

    text.append("tspan")
        .text(d => d.data.name);

    const format = d3.format(",d");
    const tspan = text.append("tspan")
        .attr("fill-opacity", d => labelVisible(d) * 0.7)
        .text(d => ` ${format(d.value)}`);

    cell.append("title")
        .text(d => {
            return `${d.ancestors().map(d => d.data.name).reverse().join("/")}\n${format(d.value)}`;
        });

    // On click, change the focus and transitions it into view.
    let focus = root;
    function clicked(event, p) {
        focus = focus === p ? p = p.parent : p;

        root.each(d => d.target = {
            x0: (d.x0 - p.x0) / (p.x1 - p.x0) * height,
            x1: (d.x1 - p.x0) / (p.x1 - p.x0) * height,
            y0: d.y0 - p.y0,
            y1: d.y1 - p.y0
        });

        const t = cell.transition().duration(750)
            .attr("transform", d => `translate(${d.target.y0},${d.target.x0})`);

        rect.transition(t).attr("height", d => rectHeight(d.target));
        text.transition(t).attr("fill-opacity", d => +labelVisible(d.target));
        tspan.transition(t).attr("fill-opacity", d => labelVisible(d.target) * 0.7);
    }

    function rectHeight(d) {
        return d.x1 - d.x0 - Math.min(1, (d.x1 - d.x0) / 2);
    }

    function labelVisible(d) {
        return d.y1 <= width && d.y0 >= 0 && d.x1 - d.x0 > 16;
    }
}

// Fetch the data and then draw the chart
fetch('../reports/finalreport.json')
    .then(response => response.json())
    .then(data => draw_icicle(data[0]));
