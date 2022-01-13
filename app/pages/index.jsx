import Head from 'next/head';
import styles from '../styles/Index.module.css';
import Main from '../components/main';
import { Button } from 'react-bootstrap';
import { Bluetooth, Gear } from 'react-bootstrap-icons';
import { Modal } from 'react-bootstrap';
import { useState } from 'react';

export default function Home() {
    // Set the state variable for the modal
    const [modalOpen, setModalOpen] = useState(false);

    const handleModalOpen = () => setModalOpen(true);
    const handleModalClose = () => setModalOpen(false);

    return (
        <div className={styles.container}>
            <Head>
                <title>Retro Magic Board</title>
            </Head>
            <div className={styles.menuBar}>
            <Button className={styles.settingsButton} variant='outline-dark' onClick={handleModalOpen}>
                <Gear />
            </Button>
            </div>
            <div className={styles.titleBar}>
                <h1 className={styles.title}>Magic Color Board</h1>
                <div className={styles.subtitle}>A board of wonders</div>
                <Main className={styles.main}/>
            </div>

            <Modal show={modalOpen} fullscreen={true} onHide={handleModalClose} className={styles.settingsModal} dialogClassName={styles.settingsModal} contentClassName={styles.modalContent} backdropClassName={styles.modalBackdrop} fullscreen={true} scrollable={true} centered>
                <Modal.Header closeButton>
                    <Modal.Title>Retroboard Settings</Modal.Title>
                </Modal.Header>
                <Modal.Body className={styles.modalBody}>
                    This is going to be where the settings exist
                </Modal.Body>
                <Modal.Footer>
                    <Button variant='outline-dark' onClick={handleModalClose}>
                        Close
                    </Button>
                    <Button variant='outline-dark' onClick={handleModalClose}>
                        Save Changes
                    </Button>
                </Modal.Footer>
            </Modal>
        </div>
    );
}
