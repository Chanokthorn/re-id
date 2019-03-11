import React, { Component } from "react";
import styled from "styled-components";
import PropTypes from 'prop-types';

const SliderStyle = styled.div`
display: flex;
align-items: center;
padding: 5px;

.output {
    background: ${p => p.color};
    color: #fff;
    border-radius: 2px;
    padding: 3px 7px;
    margin: 0px 10px;
    text-align: center;
    position: relative;
    &::before {
        content: '';
        position: absolute;
        left: -12px;
        top: 50%;
        transform: translateY(-50%);
        height: 0;
        width: 0;
        border: solid 6px ${p => p.color};
        z-index: -1;
        border-top-color: white;
        border-bottom-color: white;
        border-left-color: white;
    }
}

/* CHROME */
.range {
    -webkit-appearance: none;
    outline: none;
    background: ${p => p.color};
    height: 6px;
    width: 200px;
    border-radius: 5px;
    &::-webkit-slider-thumb {
        -webkit-appearance: none;
        width: 18px;
        height: 18px;
        border-radius: 50%;
        background: ${p => p.color};
    }
}

/* FIREFOX */
.range::-moz-range-thumb {
    border: none;
    height: 14px;
    width: 14px;
    border-radius: 50%;
    background: ${p => p.color};
    cursor: pointer;
}

.range::-moz-range-track {
    width: 100%;
    height: 3px;
    cursor: pointer;
    background: ${p => p.color};
    border-radius: 5px;
}
`;

class Slider extends Component {
    constructor(props) {
        super(props);
        this.updateRange = this.updateRange.bind(this);
    }

    updateRange = (e) => {
        this.props.updateRange(parseFloat(e.target.value));
    }

    render() {
        const { range, min, max, step } = this.props;
        return (
            <SliderStyle
                color={"#2AA3FF"}
            >
                <input
                    className="range"
                    type="range"
                    value={range}
                    min={min}
                    max={max}
                    step={step}
                    onChange={this.updateRange}
                />
                <span className="output">{range}</span>
            </SliderStyle>
        )
    }
}

export default Slider;

Slider.propTypes = {
    updateRange: PropTypes.func,
    range: PropTypes.number.isRequired,
    min: PropTypes.number.isRequired,
    max: PropTypes.number.isRequired,
    step: PropTypes.number.isRequired
}