import React from 'react';
import { useState, useEffect } from 'react';
import styles from '../styles/AppSettings.module.css';
import { Dialog, DialogContent, DialogTitle, DialogActions, Button, Autocomplete, Chip, TextField, getRadioUtilityClass } from '@mui/material';
import { localIP } from './config';

export default function AppSettings(props) {
	const [scroll, setScroll] = useState('paper');
	const [graphType, setGraphType] = useState();
	const [symbol, setSymbol] = useState();

	const graphTypeList = ['filled', 'bar', 'diff'];

	function changeGraphType(e, val) {
		setGraphType(val);
		let settings_copy = Object.assign({}, props.settings);
		settings_copy.ticker.graph_type = val;
		props.setSettings(settings_copy);
	}

	function changeSymbol(e) {
		const s = e.target.value
		setSymbol(s);
		let settings_copy = Object.assign({}, props.settings);
		settings_copy.ticker.symbol = s;
		props.setSettings(settings_copy);
	}

	function sendSettings(e) {
		e.preventDefault();
		const requestOptions = {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(props.settings),
		};
		fetch('http://' + localIP + '/api/settings', requestOptions);
		props.handleAppSettingsClose();
	}

	useEffect(() => {
		fetch('http://' + localIP + '/api/settings')
			.then((res) => res.json())
			.then((data) => {
				props.setSettings(data);
				setGraphType(data.ticker.graph_type);
				setSymbol(data.ticker.symbol);
			});
	}, [props.resetSettings]);

	return (
		<div className={styles.container}>
			<Dialog
				open={props.appSettingsOpen}
				onClose={props.handleAppSettingsClose}
				scroll={scroll}
				aria-labelledby="scroll-dialog-title"
				aria-describedby="scroll-dialog-description"
				className={styles.dialog}
			>
				<DialogTitle>{props.app} Settings</DialogTitle>
				<form onSubmit={sendSettings}>
				<DialogContent className={styles.settingsBody} >
					<div className={styles.settingsContainer}>
						<Autocomplete
							disablePortal
							className={styles.textBox}
							id='color-mode-selector'
							options={graphTypeList}
							sx={{ width: 200 }}
							onChange={(e, val) => changeGraphType(e, val)}
							renderInput={(params) => (
								<TextField {...params} label='Graph Type' />
							)}
						/>
						<Chip label={graphType} variant='outlined' />
					</div>
					<div className={styles.settingsContainer}>
						<TextField className={styles.textBox} sx={{ width: 200 }} id='symbol-text-field' label='Symbol' onChange={(e) => changeSymbol(e)}/>
						<Chip label={symbol} variant='outlined' />
					</div>
				</DialogContent>
				<DialogActions>
					<Button
						className={styles.button}
						variant='outlined'
						color='error'
						type='button'
						onClick={() => props.setResetSettings(!props.resetSettings)}
					>
						Reset
					</Button>
					<Button
						className={styles.button}
						variant='outlined'
						type='button'
						onClick={props.handleAppSettingsClose}
					>
						Close
					</Button>
					<Button 
					className={styles.button}
					variant='outlined' 
					color='success'
					onClick={sendSettings}
					type='submit'
					autoFocus>
						Save Changes
					</Button>
				</DialogActions>
				</form>
			</Dialog>
		</div>
	);
}