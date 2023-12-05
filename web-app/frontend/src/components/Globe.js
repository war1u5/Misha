import PropTypes from 'prop-types';
import React from 'react';
import createReactClass from 'create-react-class';
import data from '../assets/world-110m.json';
import {easeCubicInOut} from 'd3-ease';
import {feature} from 'topojson-client';
import {geoCircle, geoOrthographic, geoPath} from 'd3-geo';
import {interpolate} from 'd3-interpolate';

const land = feature(data, data.objects.land);

const Globe = createReactClass({
  "propTypes": {
    "center": PropTypes.array.isRequired,
    "diameter": PropTypes.number.isRequired,
    "landColor": PropTypes.string.isRequired,
    "markerColor": PropTypes.string.isRequired,
    "markerRadius": PropTypes.number.isRequired,
    "oceanColor": PropTypes.string.isRequired,
    "onClick": PropTypes.func,
    "rotationTime": PropTypes.number.isRequired,
  },

  "getDefaultProps"() {
    return {
      "center": [0, 0],
      "diameter": 541,
      "landColor": '#000000',
      "markerColor": '#009da5',
      "markerRadius": 0,
      "oceanColor": '#ffffff',
      "rotationTime": 100,
    };
  },

  "componentDidMount"() {
    this.update();
  },

  "componentDidUpdate"(prevProps) {
    if (
      prevProps.diameter !== this.props.diameter ||
      prevProps.landColor !== this.props.landColor ||
      prevProps.markerColor !== this.props.markerColor ||
      prevProps.markerRadius !== this.props.markerRadius ||
      prevProps.oceanColor !== this.props.oceanColor
    ) {
      this.update();
    }
    if (prevProps.center !== this.props.center) {
      this.recenter();
    }
  },

  "update"() {
    const diameter = this.props.diameter;
    const radius = diameter / 2;

    const projection = geoOrthographic()
      .scale(radius - 2)
      .translate([radius, radius])
      .rotate(this.props.center.map(value => -value))
      .clipAngle(90);

    this.renderPath = geoPath()
      .projection(projection)
      .context(this.canvas.getContext('2d'));

    this.projection = projection;

    this.renderGlobe();
  },

  "recenter"() {
    const start = Date.now();
    const duration = this.props.rotationTime;

    const getRotation = interpolate(
      this.projection.rotate(),
      this.props.center.map(value => -value)
    );

    const updateRotation = () => {
      const progress = Math.min(1, (Date.now() - start) / duration);
      this.projection.rotate(getRotation(easeCubicInOut(progress)));
      this.renderGlobe();
      if (progress < 1) {
        this.transition = requestAnimationFrame(updateRotation);
      }
    };

    if (this.transition) {
      cancelAnimationFrame(this.transition);
      delete this.transition;
    }

    this.transition = requestAnimationFrame(updateRotation);
  },

  "renderGlobe"() {
    if (!this.canvas) {
      if (this.transition) {
        cancelAnimationFrame(this.transition);
      }
      return;
    }

    const context = this.canvas.getContext('2d');
    context.clearRect(0, 0, this.canvas.width, this.canvas.height);

    context.fillStyle = this.props.oceanColor;
    context.beginPath();
    this.renderPath({"type": 'Sphere'});
    context.fill();

    context.fillStyle = this.props.landColor;
    context.beginPath();
    this.renderPath(land);
    context.fill();

    const circle = geoCircle()
      .center(this.props.center)
      .radius(this.props.markerRadius)();
    context.fillStyle = this.props.markerColor;
    context.beginPath();
    this.renderPath(circle);
    context.fill();
  },

  "render"() {
    const style = {"cursor": this.props.onClick ? 'pointer' : 'auto'};

    return (
      <div className="pl-globe" onClick={this.props.onClick} style={style}>
        <canvas
          height={this.props.diameter}
          ref={canvas => {
            this.canvas = canvas;
          }}
          width={this.props.diameter}
        />
      </div>
    );
  },
});

export default Globe;