(function (global, factory) {
    typeof exports === 'object' && typeof module !== 'undefined' ? factory(exports, require('d3'), require('XRegExp'), require('d3array')) :
    typeof define === 'function' && define.amd ? define(['exports', 'd3', 'XRegExp', 'd3array'], factory) :
    (global = typeof globalThis !== 'undefined' ? globalThis : global || self, factory(global.eccoBundle = {}, global.d3, global.XRegExp, global.d3array));
}(this, (function (exports, d3, XRegExp, d3array) { 'use strict';

    function _interopDefaultLegacy (e) { return e && typeof e === 'object' && 'default' in e ? e : { 'default': e }; }

    var XRegExp__default = /*#__PURE__*/_interopDefaultLegacy(XRegExp);

    function token_styler(selection) {
        // console.log('styler:', selection, typeof (selection), typeof ('hi'))
        selection
            .classed('token', function (d, i) {
                return true
            })
            .classed('new-line', function (d, i) {
                // console.log('nl', d, d == '\n')
                return d.token === '\n' || d.token === '\n\n' ; // True if new line
            })
            .classed('token-part', function (d, i) {
                // If the first character is a space, then this is a partial token
                // Except if the token only has one character
                if (d.token.length > 1 && d.token[0] !== ' ')
                    return true
                    // If a single letter, then it's part of the preceeding word
                    // This is especially the case with WordPiece, where "It" is
                // broken into the tokens "_T" and "t"
                else if ((d.token.length === 1) && XRegExp__default['default']("^\\pL+$").test(d.token)) {
                    return true
                } else
                    return false

            })
            .classed('input-token', function (d, i) {
                return d.type === 'input';
            })
            .classed('output-token', function (d, i) {
                return d.type === 'output';
            });
    }

    function display_token(token) {
        if (token === ' ') {
            return '\xa0'
        }
        if (token === '\n') { // Was: '\n'
            // console.log('new line')
            return '\\n'
        }

        if (token === '\n\n') { // Was: '\n'
            // console.log('new line')
            return '\\n\\n'
        }
        return token
    }

    class TextHighlighter {

        constructor(_config = {}) {
            this.config = {
                // Controls for color of background
                bgColorScaler: _config.bgColorScaler ||
                    d3.scaleLinear().domain([0.2, 1]).range([0, 0.5]),
                bgColorInterpolator: _config.bgColorInterpolator ||
                    d3.interpolateRgb("white", "blue"),

                // Controls for color of token text
                textColorScaler: _config.textColorScaler ||
                    d3.scaleLinear()
                        .domain([0,1])
                        .range([0, 1]),
                textColorInterpolator: _config.textColorInterpolator,



                // display the number of the position in sequence. Default true
                showPosition:(typeof _config.showPosition !== "undefined")?
                    _config.showPosition : true, // Value could be 'false', this is to accommodate

                overrideTokenBorderColor: _config.overrideTokenBorderColor, // Okay to be undefined

                // The data object will a 'tokens' list and another member e.g. 'attributions'
                // or 'factors'. We declare its name here so we can retrieve the values.
                valuesKey: _config.valuesKey || 'values',

                // Flag used to control highlight animation in bgColor()
                overrideColorParam: false
            };

            this.parentDivId = _config.parentDiv;
            this.data = _config.data;

        }


        init() {
            this.div = d3.select('#' + this.parentDivId);
            this.innerDiv = this.div.append('div');


            this.innerDiv.style('float', 'left')
                .style('float', 'left')
                .style('width', '70%');
            // Construct token boxes, most of the work is done here
            const token_boxes = this.setupTokenBoxes(this.data['tokens']);


            // Show where inputs start
            this.innerDiv
                .insert('div', ':first-child')//Insert at the beginning
                .attr('class', 'sequence-indicator inputs-indicator')
                .html('input:');

            // Show where the output sequence starts
            this.innerDiv
                .insert('div', '.output-token') //Insert before the first output token
                .attr('class', 'sequence-indicator outputs-indicator')
                .html('output:');

        }


        setupTokenBoxes(tokenData) {
            const self = this;
            let token_boxes = this.innerDiv.selectAll('div.token')
                .data(tokenData, (d, i) => {
                    return d['position'] //The position of the token is its key
                })
                .join(enter =>
                        enter.append('div')
                            .attr('token', (d, i) => {
                                return d.token
                            })
                            .attr('id', (d, i) => 't' + i)
                            .attr('position', (d, i) => i)
                            .attr('value', (d, i) => d.value || 0)
                            .style('opacity', 0)
                            .style('background-color', (d, i) => {
                                // console.log("bg", d, d.value)
                                return self.bgColor(d)
                            })
                            .style('border-color', () => {
                                if (self.config.overrideTokenBorderColor)
                                    return self.config.overrideTokenBorderColor
                                // If not set, don't return anything, let it fallback to CSS definition
                            })
                            .call(token_styler)
                            // Set up the children of the box
                            .each(function (d, i) {

                                // Position in the sequence
                                if( self.config.showPosition ){
                                    d3.select(this).append('div')
                                        .attr('class', 'position_in_seq')
                                        .text(() => i);
                                }
                                // Token Text
                                d3.select(this).append('span')
                                    .text(() => display_token(d.token))
                                    .style('color', (d, i) => self.textColor(d.value))
                                    .style('padding-left', '4px');

                            })
                            .call(enter => enter.transition().duration(500)
                                .style('opacity', 1))

                            ,
                    update => update
                        .style('background-color', (d) => {
                                return self.bgColor(d)
                            })
                        // .each(function (d) {
                        // })
                );// End Join
        }

        // Get the background
        bgColor(token) {
            // If token explicitly has a color, use that
            // Case: using different colors for different factors in one view
            // console.log('bgColor',(!this.config.overrideColorParam) ,  (token.color !== undefined))
            if ((!this.config.overrideColorParam) && (token.color !== undefined)){
                return token.color
            }
            // If no explicit color, interpolate using value
            else if (token.value !== undefined)
                return this.config.bgColorInterpolator(
                    this.config.bgColorScaler(token.value))
            // If no Value, white background
            else
                return "white"
        };

        textColor(value) {
            const scaledValue = this.config.textColorScaler(value);
            if (this.config.textColorInterpolator) {
                return this.config.textColorInterpolator(scaledValue)
            }
            // else if (scaledValue > 0.4)
            //     return '#ffffff'
            else
                return '#000000'
        };


        updateData(id, color = null) {
            const newValues = this.data[this.config.valuesKey][0][id];

            // let max = this.data['tokens'][0].value
            // Update the 'value' parameter of each token
            // So when self.setupTokenBoxes() is called, it updates
            // whatever depends on 'value' (namely, bar sparkline, and its numeric value)
            for (let i = 0; i < this.data['tokens'].length; i++) {
                this.data['tokens'][i].value = newValues[i] ? newValues[i] : 0;
                // if (this.data['tokens'][i].value > max)
                //     max = this.data['tokens'][i].value
            }

            // Update the color scale used to highlight the tokens
            if(color){
                console.log('color', color);
                this.config.bgColorInterpolator = d3.interpolateRgb("white", color);
                this.config.bgColorScaler =
                    d3.scaleLinear()
                        .domain([0,d3.max(newValues)])
                        .range([0, 1]);
            }
        }

        addToken(token){
            this.data['tokens'].push(token);
            console.log(this.data['tokens']);
        }

        redraw(){
            this.setupTokenBoxes(this.data['tokens']);
        }

    }

    class TinyChart {
        constructor(_config) {
            this.width = 20;
            this.height = 28;

            this.margin = {top: 0};
            this.numericLabelHeight = 8;
            this.barWidth = 4;
            this.barMaxHeight = this.height - this.numericLabelHeight;
            this.color = d3.interpolateViridis;

            this._scale = d3.scaleLinear()
                .domain([0, 0.4]) //TODO: This should be adjusted as a config. The whole scale

                .range([0.85, 0]); // Reversed to make low values bright
                                     // 0.2 because lower values are too bright
                                    // to be read against a white background

        }

        tinyChart(selection) {
            const self = this; // Propegate the reference to the object
                             // each will overwrite 'this'

            selection.each(function (d, i) {

                    let value = parseFloat(d.value);
                    let svg = d3.select(this)
                        .insert('svg', ':first-child')
                        .style("pointer-events", "none")
                        .attr("width", self.width)
                        .attr("height", self.height)
                        .style('margin-left','1px')
                        .style('float', 'left')
                        .append('g');

                      let normalizeHeightScale  = d3.scaleLinear()
                        .domain([0, 0.3])
                        .range([0, 1]);

                    // Probability bar
                    // console.log('prob', d.prob, 'log ', Math.log10(d.prob))
                    const prob_height = normalizeHeightScale(value * self.barMaxHeight);
                    svg.append("rect")
                        .style("pointer-events", "none")
                        .attr("y",
                            self.height - self.numericLabelHeight
                            - prob_height)
                        .attr("fill", self.color(self.scale(value)))
                        // .attr("fill", '#ec008cbb')
                        .attr("width", self.barWidth)
                        .attr("height", (d, i) => {
                            if (parseFloat(d.value) === -1)
                                return 0
                            else
                                return prob_height
                        })
                        .attr("stroke-width", 0)
                        .attr("stroke", '#333')
                        .attr("alignment-baseline", "top");

                    // Probability score text
                    const format_prob = (value * 100)
                        .toFixed(2) + '%';

                    svg.append('text')
                        .attr("x", 0)
                        .attr("y", self.barMaxHeight +
                            self.numericLabelHeight - 1)
                        .text(format_prob)
                        // .attr("fill", "#EC008Cbb")
                        .attr("fill", (d, i) => {
                            if (parseFloat(d.value) === -1)
                                return "white"
                            else
                                return self.color(self.scale(value))
                        })
                        .attr("font-family", "sans-serif")
                        .attr("font-size", "6px")
                        .attr("text-anchor", "left")
                        .attr("alignment-baseline", "top")
                        .attr('probability', value)
                        .style("pointer-events", "none");
                }
            );
        }

        scale(v){
            return this._scale(v)
        }

    }

    class TinyChartTextHighlighter extends TextHighlighter {
        constructor(_config) {
            super(_config);

            this.textColor = function (value) {
                if (this.scale(value) > 0.7)
                    return '#ffffff'
                else
                    return '#000000'
            };
        }

        init(){
            
        }

        textHighlighter(selection) {
            const self = this, tinyChart1 = new TinyChart();
            selection.each(function (d, i) {
                // console.log(33, d, this)
                // d is a list of objects, each with properties 'token' and 'value'
                // Bind token data to tokens, set token text
                let token_boxes = d3.select(this).selectAll('div')
                    .data(d, d => d['position'])
                    .join(enter => enter.append('div')
                            .style("background-color", "green"),
                        update =>update.style("background-color", "red")
                        )
                    .attr('token', (d, i) => {
                        return d.token
                    })
                    .attr('id', (d, i) => 't' + i)
                    // .attr('class', 'token')
                    .attr('position', (d, i) => i)
                    .attr('value', (d, i) => d.value || 0)
                    // .style('background-color', (d, i) => {
                    //     // console.log("9", this, self);
                    //     self.bgColor(d.value)
                    // })
                    .style('color', (d, i) =>
                        self.textColor(d.value))
                    .call(token_styler, d.token); // Add appropriate CSS classes (new line, partial token)


                // # position in the sequence
                // token_boxes
                //     .data(d)
                //     .append('div')
                //     .attr('class', 'position_in_seq')
                //     .text((d,i) => i)

                // Token text
                token_boxes.append('span')
                    .data(d=>d)
                    .text(function (d) {
                    return display_token(d.token)
                })
                    .style('margin-left', '-13px') // Makes the text closer to the tiny barchart
                    .style("pointer-events", "none");
                // Tiny bar chart
                token_boxes
                    .data(d=>d)
                    .call(tinyChart1.tinyChart.bind(tinyChart1));



                // Input sequence indicator
                d3.select(this)
                    .insert('div', ':first-child')//Insert at the beginning
                    .attr('class', 'sequence-indicator inputs-indicator')
                    .html('input:');

                // Output sequence indicator
                d3.select(this)
                    .insert('div', '.output-token') //Insert before the first output token
                    .attr('class', 'sequence-indicator outputs-indicator')
                    .html('output:');
            });
        }
    }

    class TokenSparkbarBase {
        constructor(_config = {}) {
            this.config = {
                width: _config.width || 30,
                height: _config.height || 30,
                margin: {top: 0, bottom: 0, right: 0, left: 0},
                numericLabelHeight: _config.numericLabelHeight || 10,
                barWidth: _config.barWidth || 4,
                colorInterpolator: _config.colorInterpolator || d3.interpolateViridis,
                colorScaler: _config.colorScaler ||
                    d3.scaleLinear()
                        .domain([0, 0.4]) //TODO: Change the domain when the values are set
                        .range([0.85, 0]) // Reversed to make low values bright
            };

            this.config.barMaxHeight = _config.barMaxHeight ||
                this.config.height - this.config.numericLabelHeight;
        }

        draw(selection) {
            const self=this;
            selection.each(function (d, i) {
                let value = parseFloat(d.value);
                let svg = d3.select(this)
                    .insert('svg', ':first-child')
                    // .style("pointer-events", "none")
                    .attr("width", self.config.width)
                    .attr("height", self.config.height)
                    .style('margin-left', '1px')
                    .style('float', 'left')
                    .append('g');
            });
        }

        update() {
        }
    }

    class TokenSparkbar extends TokenSparkbarBase {
        constructor(_config={}) {
            super(_config);
            this.config.normalizeHeightScale =
                _config.normalizeHeightScale ||
                d3.scaleLinear()
                    .domain([0, 0.3])
                    .range([0, 1]);
        }

        draw(selection) {
            const self = this; // Propegate the reference to the object
            // each will overwrite 'this'

            selection.each(function (d, i) {
                console.log('sparkbar', d);
                    let value = parseFloat(d.value);
                    let svg = d3.select(this)
                        .insert('svg', ':first-child')
                        // .style("pointer-events", "none")
                        .attr("width", self.config.width)
                        .attr("height", self.config.height)
                        .style('margin-left', '1px')
                        .style('float', 'left')
                        .append('g');

                    // Probability bar
                    // console.log('prob', d.prob, 'log ', Math.log10(d.prob))
                    const prob_height = self.config.normalizeHeightScale(value * self.config.barMaxHeight);
                    svg.append("rect")
                        .style("pointer-events", "none")
                        .attr("y",
                            self.config.height - self.config.numericLabelHeight
                            - prob_height)
                        .attr("fill", self.config.colorInterpolator(
                            self.config.colorScaler(value)))
                        .attr("width", self.config.barWidth)
                        .attr("height", (d, i) => {
                            if (parseFloat(d.value) === -1)
                                return 0
                            else
                                return prob_height
                        })
                        .attr("stroke-width", 0)
                        .attr("stroke", '#333')
                        .attr("alignment-baseline", "top");

                    // Probability score text
                    const format_prob = (value * 100)
                        .toFixed(2) + '%';
                    svg.append('text')
                        .attr("x", 0)
                        .attr("y", self.config.barMaxHeight +
                            self.config.numericLabelHeight - 1)
                        .text(value == 0? '': format_prob)
                        // .attr("fill", "#EC008Cbb")
                        .attr("fill", (d, i) => {
                            if (parseFloat(d.value) === -1)
                                return "white"
                            else
                                return self.config.colorInterpolator(
                                    self.config.colorScaler(value))
                        })
                        .attr("font-family", "sans-serif")
                        .attr("font-size", "10px")
                        .attr("text-anchor", "left")
                        .attr("alignment-baseline", "top")
                        .attr('probability', value);
                        // .style("pointer-events", "none")
                }
            );
        }

        update(selection) {
            const self = this;

            selection.each(function (d, i) {
                let value = parseFloat(d.value);
                const prob_height = self.config.normalizeHeightScale(
                    value * self.config.barMaxHeight);
                var t = d3.transition()
                    .duration(100)
                    .ease(d3.easeLinear);

                // Update bar chart
                let rect = d3.select(this).select('rect');
                rect.transition(t)
                    .attr("fill", self.config.colorInterpolator(self.config.colorScaler(value)))
                    .attr("y",
                        self.config.height - self.config.numericLabelHeight
                        - prob_height)
                    .attr("height", (d, i) => {
                        if (parseFloat(d.value) === -1)
                            return 0
                        else
                            return prob_height
                    });

                // Update score text
                const format_prob = (value * 100)
                    .toFixed(2) + '%';
                let text = d3.select(this).select('text');
                text.text(value === 0? '': format_prob)
                    .attr("fill", (d, i) => {
                        if (parseFloat(d.value) === -1)
                            return "white"
                        else
                            return self.config.colorInterpolator(
                                self.config.colorScaler(value))
                    });
            });
        }

        scale(v) {
            return this._scale(v)
        }

    }

    class InteractiveTokenSparkbar extends TextHighlighter {
        constructor(_config) {
            super(_config);

        }

        init() {
            console.log('data 0', this.data);
            this.tokenSparkline = new TokenSparkbar();
            this.div = d3.select('#' + this.parentDivId);
            this.innerDiv = this.div.append('div');

            const self = this,
                // Construct token boxes, most of the work is done here
                token_boxes = this.setupTokenBoxes(self.data['tokens']);

            // Hover listeners
            this.innerDiv.selectAll('div.output-token')
                .style('border','1px dashed purple')
                .on("mouseenter", (d, i)=>{
                    self.hover(d,i);
                })
                .on("touchstart", (d,i)=>{
                    self.hover(d,i);
                });

            // Input sequence indicator
            this.innerDiv
                .insert('div', ':first-child')//Insert at the beginning
                .attr('class', 'sequence-indicator inputs-indicator')
                .html('input:');

            // Output sequence indicator
            this.innerDiv
                .insert('div', '.output-token') //Insert before the first output token
                .attr('class', 'sequence-indicator outputs-indicator')
                .html('output:');
        }

        hover(d,i){
            const self = this;
            console.log('hover', i);
            let disableHighlight = self.innerDiv.selectAll(`[highlighted="${true}"]`)
                .style('border', '1px dashed purple')
                .attr('highlighted', false)
                .style('background-color', '');
            let s = self.innerDiv.selectAll(`[position="${d.position}"]`)
                .attr('highlighted', true)
                .style('border', '1px solid #8E24AA')
                .style('background-color', '#E1BEE7');
            self.updateData(i);
            self.setupTokenBoxes(self.data['tokens']);
        }

        selectFirstToken() {
            const firstTokenId = this.innerDiv.select('.output-token').attr('position');
            console.log('firstTokenId', firstTokenId);
            this.hover({position: firstTokenId}, 4);
        }

        setupTokenBoxes(tokenData) {
            //
            const self = this;
            const bgScaler = d3.scaleLinear()
                .domain([0, 1]) //TODO: Change the domain when the values are set
                .range([1, 0]);
            const token_boxes = this.innerDiv.selectAll('div.token')
                .data(tokenData, (d, i) => {
                    return d['position']
                })
                .join(
                    enter =>
                        enter.append('div')
                            .attr('token', (d, i) => {
                                return d.token
                            })
                            .attr('id', (d, i) => 't' + i)
                            .attr('position', (d, i) => i)
                            .attr('value', (d, i) => d.value || 0)
                            .style('color', (d, i) =>
                                self.textColor(d.value))
                            .style('background-color', (d) => {
                                // return self.bgColor(d)
                                }
                            )
                            .call(token_styler)
                            .each(function (d) {
                                d3.select(this).append('span')
                                    .text(function (d) {
                                        return display_token(d.token)
                                    })
                                    .style('margin-left', '-13px') // Makes the text closer to the tiny barchart
                                    .style("pointer-events", "none");

                                d3.select(this)
                                    .call(self.tokenSparkline.draw.bind(self.tokenSparkline));
                            }),
                    update => update
                        .each(function (d) {
                                d3.select(this).call(self.tokenSparkline.update.bind(self.tokenSparkline));
                            }
                        ));

            return token_boxes
        }

        updateData(attribution_list_id) {
            console.log('data', this.data);
            console.log('updateData', attribution_list_id);
            const newValues = this.data['attributions'][attribution_list_id];
            console.log('newValues', newValues, this.data['attributions']);
            let max = this.data['tokens'][0].value;
            // Update the 'value' parameter of each token
            // So when self.setupTokenBoxes() is called, it updates
            // whatever depends on 'value' (namely, bar sparkline, and its numeric value)
            for (let i = 0; i < this.data['tokens'].length; i++) {
                this.data['tokens'][i].value = newValues[i] ? newValues[i] : 0;
                if (this.data['tokens'][i].value > max)
                    max = this.data['tokens'][i].value;
            }

            // Set the max value as the new top of the domain for the sparkline
            // -- Both for color and for bar height
            this.tokenSparkline.config.colorScaler = d3.scaleLinear()
                .domain([0, max])
                .range(this.tokenSparkline.config.colorScaler.range());
            // console.log('UPDATING DOMAIN', this.tokenSparkline.config.colorScaler.domain())

            this.tokenSparkline.config.normalizeHeightScale = d3.scaleLinear()
                .domain([0, max])
                .range(this.tokenSparkline.config.normalizeHeightScale.range());
        }
    }

    // Reference: https://observablehq.com/d/9d7507ca9c029767
    class ActivationSparklineBase {
        constructor(_config = {}) {
             // console.log(_config)
            // this.config.margin =  _config.margin ||
            //     {top: 50, right: 30, bottom: 30, left: 60}, // Default value
            this.config = {
                margin: _config.margin ||
                    {top: 50, right: 30, bottom: 30, left: 30},

                // The higher the value, the more the lines would overlap
                // Lower values are problematic if we show only 3-5 lines
                overlap: _config.overlap || 0.3,

            };

            this.config['height'] = _config.height ||
                200 +
                d3.min([500, 20 * _config.data['factors'][0].length]) // Scale according to the number of factors,
                // but only up to 400
                - this.config.margin.top
                - this.config.margin.bottom;

            this.config['width'] = _config.width ||
                350 - this.config.margin.left - this.config.margin.right;

            // 350 - this.config.margin.left - this.config.margin.right

            this.parentDivId = _config.parentDiv;
            this.data = _config.data;
        }

        init() {
            const self = this,
                factors = this.data['factors'][0],
                n_factors = factors.length;


            // var margin = {top: 50, right: 30, bottom: 30, left: 60},
            //     width = 350 - margin.left - margin.right,
            //     height = 400 + 15*n_factors - margin.top - margin.bottom;

            this.div = d3.select('#' + this.parentDivId);
            this.innerDiv = this.div.append('div')
                .attr('id', 'activation-sparklines')
                .style('float', 'left')
                .style('width', '25%');
            this.svg = this.innerDiv.append('svg')
                .attr("viewBox", [0, 0, this.config.width, this.config.height]);


            this.lineColors = d3.scaleSequential()
                .domain([0, factors.length])
                // .range([0.1,1])
                .interpolator(d3.interpolateRainbow);
            // console.log('interpolate', this.lineColors(0))

            var x = d3.scaleLinear()
                .domain([0, factors[0].length])
                .range([this.config.margin.left,
                    this.config.width - this.config.margin.right]);

            // Scale to place each line chart vertically in the right place
            var y_lines = d3.scalePoint()
                .domain(factors.map((d, i) => i)) // List of chart ids e.g. [0,1,2]

                .range([this.config.margin.top,
                    this.config.height - this.config.margin.bottom]);

            // The y axis interploator for the line/area path
            const z = d3.scaleLinear()
                .domain([
                    d3.min(factors, d => d3.min(d)),
                    d3.max(factors, d => d3.max(d)) / 2
                ])
                .range([0,  -self.config.overlap *y_lines.step()]);//

            let line = d3.line()
                .curve(d3.curveCardinal)
                .x((d, i)=> x(i) )
                .y((d)=> z(d));

            const groups = this.svg.selectAll('g')
                .data(factors)
                .join('g') // Create an svg group for each factor
                .attr('transform', (d, i) => {
                        // console.log('y_lines(i)', i, y_lines(i))
                        return `translate(0, ${y_lines(i)})`
                    }
                ); // Move to the appropriate height


            // Area under the line
            const area = d3.area()
                .defined(d => !isNaN(d))
                .x((d, i) => x(i))
                .y0(0)
                .y1(z);
            // groups.append("path")
            //     .attr("fill", (d, i) => this.lineColors(i))
            //     .attr("opacity", 0.2)
            //     .attr("d", area);
            groups.append('text')
                // .attr('y', -y_lines.step()/2)
                // .attr('x' ,-5)
                .attr('fill', (d, i) => this.lineColors(i) )
                .attr('font-size', '20px')
                .text((d,i)=>i+1);

            // Draw the visibile line
            groups.append('path')
                .attr("fill", "none")
                .attr("stroke-width", 2)
                .attr("stroke", (d, i) => this.lineColors(i))
                .attr("d", line);

            // Draw another line, same path, but fatter so interaction is easier
            groups.append('path')
                .attr("fill", "none")
                .attr("opacity", 0)
                .attr("stroke-width", 30)
                .attr("stroke", (d, i) => this.lineColors(i))
                .attr("d", line)
                .on("mouseenter",  (d, i)=> {
                    self.hover(i, self.lineColors(i));
                })
                .on("touchstart",  (d, i)=> {
                    self.hover(i, self.lineColors(i));
                })
                .on('mouseleave', (d,i)=>{
                    self.hoverEnd(i, self.lineColors(i));
                });
                // .on('touchend', (d,i)=>{
                //     self.hoverEnd(i, self.lineColors(i))
                // })

            // Bottom axis, I think
            this.svg.append("g")
                .attr("transform", `translate(0,${ 
                this.config.height- this.config.margin.bottom  })`)
                .call(d3.axisBottom(x).ticks(5));
        }

        hover(id, color) {
            this.hoverAction(id, color);
        }


        hoverEnd(id, color) {
            this.hoverEndAction(id, color);
        }
    }

    function renderOutputSequence(parent_div, data) {

        const highlighter = new TextHighlighter({
            parentDiv: parent_div,
            data: data
        });
        highlighter.init();

        return highlighter;
    }


    function renderSeqHighlightPosition(parent_div, position, data) {

        const div = d3.select('#' + parent_div),
            n_tokens = data['tokens'].length,
            highlighter = new TinyChartTextHighlighter();
        // highlighter = new TinyChartTextHighlighter();
        // highlighter.textHighlighter([1])

        let selection = div.selectAll('div')
            .data([data['tokens']])
            .join('div')
            .call(highlighter.textHighlighter.bind(highlighter)); // Binding, otherwise 'this' is overwritten

        // Highlight the selected token
        let s = d3.selectAll(`[position="${position}"]`)
            .style('border', '1px solid #8E24AA');
        highlighter.init();
        console.log('Selection', selection, s);
    }

    // Small bar next to each token. Change their value upon hovering on output
    // tokens (to visualize attribution
    function interactiveTokens(parent_div, data) {
        const tokenChart = new InteractiveTokenSparkbar({
            parentDiv: parent_div,
            data: data,
        });

        tokenChart.init();
        tokenChart.selectFirstToken();
        // tokenChart.hover({},0)
    }

    // Shows tokens with highlighted bg colors based on value
    function bgHighlighterSequence(parent_div, data) {
        const highlighter = new TextHighlighter({
            parentDiv: parent_div,
            data: data,
            showPosition: false,
            overrideTokenBorderColor: 'white'
        });

        highlighter.init();
    }


    function interactiveTokensAndFactorSparklines(parent_div, data, _config = {}) {

        // console.log('data', data)
        window.d = data;

        // Draw the sparkline line-charts for factor activations
        const activationSparkline = new ActivationSparklineBase({
            ..._config['actSparklineCFG'],
            parentDiv: parent_div,
            data: data
        });

        activationSparkline.init();

        // Draw the tokens showing the activations
        const highlighter = new TextHighlighter({
            ..._config['hltrCFG'],
            parentDiv: parent_div,
            data: data,
            showPosition: false,
            overrideTokenBorderColor: 'white',
            valuesKey: 'factors'
        });


        let mostPronounceFactorPerToken = [];
        // for each token
        data['tokens'].map((d, i) => {
            // Find the factor that has the highest activation value for the token
            // save the factor id
            mostPronounceFactorPerToken.push(
                d3array.maxIndex(
                    data['factors'][0], (f) => f[i]));
        });
        // console.log('3', mostPronounceFactorPerToken)

        let factorColorInterpolators = [];
        let factorColorScalers = [];
        data['factors'][0].map((values, i) => {
            let color = activationSparkline.lineColors(i);
            // console.log('factor:', i, ' color', color)
            factorColorInterpolators.push(d3.interpolateRgb("white", color));
            factorColorScalers.push(d3.scaleLinear()
                .domain([0, d3.max(values)])
                .range([0, 1]));
        });
        // console.log('4', factorColorInterpolators, factorColorScalers)
        // Update token color values
        for (let i = 0; i < data['tokens'].length; i++) {
            let factor_id = mostPronounceFactorPerToken[i];
            // console.log('4.5', i, factor_id,
            //     'value:', data['factors'][0][factor_id][i],
            //     'scaled value: ', factorColorScalers[factor_id](
            //         data['factors'][0][factor_id][i]
            //     ),
            //     'interpolated scaled value:',
            //     factorColorInterpolators[factor_id](
            //         factorColorScalers[factor_id](
            //             data['factors'][0][factor_id][i]
            //         )
            //     )
            // )
            data['tokens'][i]['color'] =
                factorColorInterpolators[factor_id](
                    factorColorScalers[factor_id](
                        data['factors'][0][factor_id][i]
                    )
                );
        }
        // console.log('6 ', data['tokens'])

        highlighter.init();
        activationSparkline.hoverAction = function (id, color) {
            highlighter.config.overrideColorParam = true;
            // When hovering on a line chart, show its values on the tokens
            highlighter.updateData(id, color);
            highlighter.redraw();
        };

        activationSparkline.hoverEndAction = function (id, color) {
            // console.log('HOVER END')
            highlighter.config.overrideColorParam = false;
            // When hovering on a line chart, show its values on the tokens
            // highlighter.updateData(id, color)
            highlighter.redraw();
        };
    }

    exports.InteractiveTokenSparkbar = InteractiveTokenSparkbar;
    exports.TextHighlighter = TextHighlighter;
    exports.TinyChartTextHighlighter = TinyChartTextHighlighter;
    exports.TokenSparkbar = TokenSparkbar;
    exports.TokenSparkbarBase = TokenSparkbarBase;
    exports.bgHighlighterSequence = bgHighlighterSequence;
    exports.interactiveTokens = interactiveTokens;
    exports.interactiveTokensAndFactorSparklines = interactiveTokensAndFactorSparklines;
    exports.renderOutputSequence = renderOutputSequence;
    exports.renderSeqHighlightPosition = renderSeqHighlightPosition;

    Object.defineProperty(exports, '__esModule', { value: true });

})));
