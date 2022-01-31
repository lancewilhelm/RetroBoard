import React, { useState } from 'react';
import { SketchPicker } from 'react-color';
import { GradientPickerPopover } from 'react-linear-gradient-picker';
import 'react-linear-gradient-picker/dist/index.css';
import '../styles/GradientButton.module.css';

export default function GradientButton(props) {
    const [open, setOpen] = useState(false);
    const [angle, setAngle] = useState(90);

    const rgbToRgba = (rgb, a = 1) =>
    rgb.replace('rgb(', 'rgba(').replace(')', `, ${a})`);

    const WrappedSketchPicker = ({ onSelect, ...rest }) => {
        return (
            <SketchPicker
                {...rest}
                color={rgbToRgba(rest.color, rest.opacity)}
                onChange={(c) => {
                    const { r, g, b, a } = c.rgb;
                    onSelect(`rgb(${r}, ${g}, ${b})`, a);
                }}
            />
        );
    };

    return (
        <GradientPickerPopover 
            {...{
                open,
                setOpen,
                angle,
                setAngle,
                showAnglePicker: true,
                width: 220,
                maxStops: 2,
                paletteHeight: 32,
                palette: props.gradPalette,
                onPaletteChange: props.updateGradPalette
            }}
        >
            <WrappedSketchPicker />
        </GradientPickerPopover>
    );
};