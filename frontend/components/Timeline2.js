import React, { Component } from "react";
import styled from "styled-components";
import PropTypes from 'prop-types';
import { get } from "lodash";
import Slider from "./Slider";

const TimelineStyle = styled.section`
position: relative;
margin: 0px 20px;
width: calc(100vw - 2*20px);
overflow: hidden;

section {
    box-sizing: border-box;
    /* padding: 10px 20px; */
    width: calc(100vw - 2*20px);
    overflow-x: scroll;

    table {
        margin-left: 150px;

        .hard-bar {
            position: absolute;
            height: 100%;
            border-left: 1px solid #000;
            top: 0px;
            z-index: 3;
        }

        .video-item {
            display: table-row;
            height: 50px;

            .video-name {
                line-height: 50px;
                min-width: 150px;
                max-width: 150px;
                height: 50px;
                text-align: center;
                position: absolute;
                left: 0px;
                z-index: 5;
                background: white;
            }
            
            .video-timeline-wrapper {
                background-color: #EEE;
                position: relative;
                box-sizing: border-box;
                padding: 0px 10px;
                transition: all 0.2s ease-in-out;
                height: 50px;

                &:hover {
                    background-color: #CCC !important;
                }
                &.active {
                    background: #C5C5C5 !important;
                }
                &:active {
                    background-color: #999 !important;
                }

                .video-timeline {
                    .video-lifeline {
                        box-sizing: border-box;
                        height: 15px;
                        background: #2A7EFF;
                        position: relative;

                        .video-highlight {
                            height: 25px;
                            top: 0;
                            transform: translateY(-5px);
                            background: #FFC148;
                            border-radius: 3px;
                            border: 1px solid #0001;
                            position: absolute;
                            .bubble {
                                display: none;
                            }
                            &:hover {
                                border: 2px solid yellow;
                                .bubble {
                                    display: block;
                                    background: #FFF;
                                    padding: 5px;
                                    box-sizing: border-box;
                                    transform: translateY(-30px);
                                }
                            }
                            display: flex;
                            justify-content: center;
                            align-items: center;

                        }
                    }
                }
            }

            &:nth-child(2) {
                .video-timeline-wrapper:hover {
                    height: 100px;
                }
            }

            &:nth-child(2n) {
                .video-timeline-wrapper {
                    background-color: #E1E1E1;
                }
                .video-name {
                    background: #F3F3F3;
                }
            }
        }
    }
}

.no-height {
    height: 0px !important;
    line-height: 0px !important;
}
`;

const getRelativeCoordinates = (event, element) => {
    const position = {
        x: event.pageX,
        y: event.pageY
    };

    const offset = {
        left: element.offsetLeft,
        top: element.offsetTop
    };

    let reference = element.offsetParent;

    while (reference != null) {
        offset.left += reference.offsetLeft;
        offset.top += reference.offsetTop;
        reference = reference.offsetParent;
    }

    return {
        x: position.x - offset.left + element.scrollLeft,
        y: position.y - offset.top,
    };
}

const mergeStack = (callbacks) => (...args) => {
    callbacks.forEach((callback) => callback(...args));
};

const RoundDecimal = (value, decimal=3) => {
    return Math.round((value * Math.pow(10, decimal))) / Math.pow(10, decimal);
}

const IndexesToRange = (indexes) => {
    if (indexes.length === 1) {
        return [[indexes[0], indexes[0]]];
    }
    let Ranges = [];
    let [startIdx, endIdx] = [indexes[0], indexes[0]];
    for (let i = 1; i < indexes.length; i++) {
        if (endIdx != indexes[i] - 1) {
            Ranges.push([startIdx, endIdx]);
            startIdx = indexes[i];
            endIdx = startIdx;
        } else {
            endIdx = indexes[i];
        }
    }
    Ranges.push([startIdx, endIdx])
    return Ranges;
}

class Timeline extends Component {
    constructor(props) {
        super(props);
        this.state = {
            selectedIndex: -1,
            x: 10,
            scale: 10
        }
    }
    onChangeIndex = (idx) => {
        return () => {
            this.setState({
                selectedIndex: idx
            })
        }
    }
    onUpdateScale = (scale) => {
        const x = (this.state.scale === 0 || scale === 0) ? 10 : (this.state.x - 10) / (this.state.scale / scale) + 10;
        this.setState({
            scale: scale,
            x: x
        })
    }
    componentDidMount() {
        document.getElementsByTagName("body")[0].onkeydown = (e) => {
            if (e.key === "ArrowRight") {
                this.setState({
                    x: Math.min(this.state.x + 1, this._Timeline.children[0].children[0].offsetWidth - 10)
                })
            } else if(e.key === "ArrowLeft") {
                this.setState({
                    x: Math.max(this.state.x - 1, 10)
                })
            }
        }
    }
    componentWillUnmount() {
        document.getElementsByTagName("body")[0].onkeydown = undefined;
    }
    calculatePamateters = (file) => {
        const secondWidth = this.state.scale;
        const { fps, offset, maxIndex, containIndex } = file;
        const timeDiff = offset - this.props.offset; // Time difference in seconds -> calculate margin
        const width = (maxIndex/fps) * secondWidth;
        
        return ({
            width: `${width}px`,
            marginLeft: `${(timeDiff/1000)*secondWidth}px`,
            containIndex: IndexesToRange(containIndex).map((it, idx) => ({
                left: `${(it[0]/maxIndex)*width}px`,
                width: `${(it[1] - it[0] + 1)/maxIndex*width}px`
            }))
        })
    }
    onUpdateBar = (e) => {
        if (this._Timeline) {
            const x = getRelativeCoordinates(e, this._Timeline).x - 150;
            this.setState({
                x: (x < 10) ? 10 : Math.min(x, this._Timeline.children[0].children[0].offsetWidth - 10) //Pixel
            })
        }
    }
    render() {
        const { selectedIndex, x, scale } = this.state;
        const { files } = this.props;
        const secondWidth = scale;
        return (
            <TimelineStyle>
                <section
                    ref={(me) => (this._Timeline = me)}
                >
                    <table>
                        <tr className="video-item no-height">
                            <th className="video-name no-height"></th>
                            <td
                                className={`video-timeline-wrapper no-height`}
                            >
                                <div
                                    className="hard-bar"
                                    style={{
                                        left: `${x}px`,
                                        height: `calc(${files.length} * 50px)`
                                    }}
                                />
                            </td>
                        </tr>
                        {
                            (files).map((it, idx) => {
                                const params = this.calculatePamateters(it);
                                return (
                                    <tr
                                        className="video-item"
                                        key={idx}
                                    >
                                        <th className="video-name">
                                            {get(it, "filename")}
                                        </th>
                                        <td
                                            className={`video-timeline-wrapper ${selectedIndex === idx ? "active" : ""}`}
                                            onClick={mergeStack([
                                                this.onChangeIndex(idx),
                                                this.onUpdateBar
                                            ])}
                                        >
                                            <div className="video-timeline">
                                                <div
                                                    className="video-lifeline"
                                                    style={{
                                                        width: params.width,
                                                        marginLeft: params.marginLeft
                                                    }}
                                                >
                                                    {
                                                        IndexesToRange(get(it, "containIndex")).map((r, index) => (
                                                            <div
                                                                className="video-highlight"
                                                                key={`highlight-${index}`}
                                                                style={{
                                                                    width: params.containIndex[index].width,
                                                                    left: params.containIndex[index].left
                                                                }}
                                                            >
                                                                <div className="bubble">
                                                                    Hello
                                                                </div>
                                                            </div>
                                                        ))
                                                    }
                                                </div>
                                            </div>
                                        </td>
                                    </tr>
                                )
                            })
                        }
                    </table>
                </section>
                <div>
                    <b>Relative Time</b> {`${RoundDecimal((secondWidth === 0) ? 0 : (x - 10)/secondWidth)} seconds`}
                </div>
                <div className="">
                    <span>
                        <b>
                            Pixels per second
                        </b>
                    </span>
                    <Slider
                        min={0}
                        max={60}
                        step={0.25}
                        updateRange={this.onUpdateScale}
                        range={scale}
                    />
                </div>
            </TimelineStyle>
        )
    }
}

export default Timeline;

const MockIndex = (ranges) => {
    // [Start, End)
    let foundIndexes = [];
    for (let i = 0; i < ranges.length; i++) {
        foundIndexes = foundIndexes.concat(Array.from(new Array(ranges[i][1] - ranges[i][0]).keys()).map((idx) => idx + ranges[i][0]))
    }
    return foundIndexes;
}

Timeline.defaultProps = {
    offset: 0,
    files: [{
        filename: "Video 1.mp4",
        offset: 0,
        fps: 23.96,
        maxIndex: 1600,
        containIndex: MockIndex([
            [0, 400],
            [700, 950],
            [960, 1200],
            [1500, 1600]
        ])
    }, {
        filename: "Video 2.mp4",
        offset: 1000*20,
        fps: 23.96,
        maxIndex: 500,
        containIndex: MockIndex([
            [20, 120],
            [450, 500]
        ])
        }, {
            filename: "Video 3.mp4",
            offset: 1000*60,
            fps: 23.96,
            maxIndex: 1600,
            containIndex: MockIndex([
                [0, 400],
                [700, 950],
                [960, 1200],
                [1500, 1600]
            ])
        }, {
            filename: "Video 4.mp4",
            offset: 1000*75,
            fps: 23.96,
            maxIndex: 1500,
            containIndex: MockIndex([
                [500, 720],
                [1200, 1500]
            ])
        }, {
            filename: "Video 5.mp4",
            offset: 1000*80,
            fps: 23.96,
            maxIndex: 1000,
            containIndex: MockIndex([
                [0, 400],
                [700, 950],
                [960, 1000]
            ])
        }, {
            filename: "Video 6.mp4",
            offset: 1000 * 135,
            fps: 23.96,
            maxIndex: 500,
            containIndex: MockIndex([
                [20, 120],
                [450, 500]
            ])
        }]
}

Timeline.propTypes = {
    offset: PropTypes.number.isRequired, // Unix-time offset
    files: PropTypes.arrayOf(PropTypes.shape({
        filename: PropTypes.string.isRequired,
        offset: PropTypes.number.isRequired,
        fps: PropTypes.number.isRequired,
        maxIndex: PropTypes.number.isRequired,
        containIndex: PropTypes.arrayOf(PropTypes.number).isRequired
    }))
}