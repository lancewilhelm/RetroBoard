import { Button } from 'react-bootstrap';
import styles from '../styles/Main.module.css';

export default function Main() {
    async function sendCommand(command) {
        const url_base = 'http://127.0.0.1:5000/api/';

        const res = await fetch(url_base + command, {
            method: 'GET',
        });
        console.log(res);
        return res;
    }

    return (
        <div className={styles.container}>
            <Button
                variant='outline-dark'
                onClick={() => sendCommand('rotate')}
            >
                Rotating Square
            </Button>
        </div>
    );
}
