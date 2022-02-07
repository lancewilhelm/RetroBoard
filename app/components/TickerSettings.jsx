import React from 'react';
import { useState, useEffect } from 'react';
import styles from '../styles/TickerSettings.module.css';
import { Dialog, DialogContent, DialogTitle, DialogActions, Button, Autocomplete, Chip, TextField, getRadioUtilityClass } from '@mui/material';
import { localIP } from './config';

export default function TickerSettings(props) {
	const [settings, setSettings] = useState({});
	const [scroll, setScroll] = useState('paper');
	const [equityType, setEquityType] = useState();
	const [graphType, setGraphType] = useState();
	const [symbol, setSymbol] = useState();
	const [symbolList, setSymbolList] = useState([]);
	const [displaySymbolList, setDisplaySymbolList] = useState([]);

	const equityTypeList = ['stock', 'crypto'];
	const graphTypeList = ['filled', 'bar'];

	const apiKeys = require('../../apikeys.json');

	function getSymbolList(type) {
        if (equityType == 'crypto') {
            fetch(
                'https://finnhub.io/api/v1/crypto/symbol?exchange=binance&token=' +
                    apiKeys.finnhub
            )
                .then((res) => res.json())
                .then((data) => {
					const display_symbol_list = data.map(a => a.displaySymbol);
					const symbol_list = data.map(a => a.symbol);
                    setSymbolList(symbol_list);
					setDisplaySymbolList(display_symbol_list);
                });
        } else {
			fetch(
                'https://finnhub.io/api/v1/stock/symbol?exchange=US&token=' +
                    apiKeys.finnhub
            )
                .then((res) => res.json())
                .then((data) => {
					const display_symbol_list = data.map(a => a.displaySymbol);
					const symbol_list = data.map(a => a.symbol);
                    setSymbolList(symbol_list);
					setDisplaySymbolList(display_symbol_list);
                });
		}
    }

	function changeEquityType(e, val) {
		setEquityType(val);
		let settings_copy = Object.assign({}, props.settings);
		settings_copy.ticker.equity_type = val;
		props.setSettings(settings_copy);
	}

	function changeGraphType(e, val) {
		setGraphType(val);
		let settings_copy = Object.assign({}, props.settings);
		settings_copy.ticker.graph_type = val;
		props.setSettings(settings_copy);
	}

	function changeSymbol(e, val) {
		const s = symbolList[displaySymbolList.indexOf(val)]
		setSymbol(s);
		let settings_copy = Object.assign({}, props.settings);
		settings_copy.ticker.symbol = s;
		props.setSettings(settings_copy);
	}

	function sendSettings() {
		const requestOptions = {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(props.settings),
		};
		fetch('http://' + localIP + ':5000/api/settings', requestOptions);
		props.handleTickerSettingsClose();
	}

	useEffect(() => {
		fetch('http://' + localIP + ':5000/api/settings')
			.then((res) => res.json())
			.then((data) => {
				props.setSettings(data);
				setEquityType(data.ticker.equity_type);
				setGraphType(data.ticker.graph_type);
				setSymbol(data.ticker.symbol);
			});
	}, [props.resetSettings]);

	useEffect(() => {
		getSymbolList();
	}, [props.tickerSettingsOpen, equityType])

	return (
		<div className={styles.container}>
			<Dialog
				open={props.tickerSettingsOpen}
				onClose={props.handleTickerSettingsClose}
				scroll={scroll}
				fullScreen={true}
				aria-labelledby="scroll-dialog-title"
				aria-describedby="scroll-dialog-description"
				className={styles.dialog}
			>
				<DialogTitle>Ticker Settings</DialogTitle>
				<DialogContent className={styles.settingsBody}>
					<div className={styles.settingsContainer}>
						<Autocomplete
							disablePortal
							className={styles.textBox}
							id='color-mode-selector'
							options={equityTypeList}
							sx={{ width: 200 }}
							onChange={(e, val) => changeEquityType(e, val)}
							renderInput={(params) => (
								<TextField {...params} label='Type' />
							)}
						/>
						<Chip label={equityType} variant='outlined' />
					</div>
					<div className={styles.settingsContainer}>
						<Autocomplete
							disablePortal
							className={styles.textBox}
							id='color-mode-selector'
							options={graphTypeList}
							sx={{ width: 200 }}
							onChange={(e, val) => changeGraphType(e, val)}
							renderInput={(params) => (
								<TextField {...params} label='Type' />
							)}
						/>
						<Chip label={graphType} variant='outlined' />
					</div>
					<div className={styles.settingsContainer}>
						<Autocomplete
							disablePortal
							className={styles.textBox}
							id='color-mode-selector'
							options={displaySymbolList}
							sx={{ width: 200 }}
							onChange={(e, val) => changeSymbol(e, val)}
							renderInput={(params) => (
								<TextField {...params} label='Type' />
							)}
						/>
						<Chip label={symbol} variant='outlined' />
					</div>
				</DialogContent>
				<DialogActions>
					<Button
						className={styles.button}
						variant='outlined'
						color='error'
						onClick={() => props.setResetSettings(!props.setResetSettings)}
					>
						Reset
					</Button>
					<Button
						className={styles.button}
						variant='outlined'
						onClick={props.handleTickerSettingsClose}
					>
						Close
					</Button>
					<Button 
					className={styles.button}
					variant='outlined' 
					color='success'
					onClick={sendSettings}>
						Save Changes
					</Button>
				</DialogActions>
			</Dialog>
		</div>
	);
}