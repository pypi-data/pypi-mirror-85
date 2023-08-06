// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';

// Import CSS
import "../../css/mito-toolbar.css"
import "../../css/margins.css"


// Import Types
import { SheetJSON } from '../widget';
import { ModalInfo, ModalEnum } from './Mito';

// Import Components 
import Tooltip from './Tooltip';

const MitoToolbar = (
    props: {
        sheetJSON: SheetJSON, 
        selectedSheetIndex: number,
        send: (msg: Record<string, unknown>) => void,
        setEditingMode: (on: boolean, column: string, rowIndex: number) => void,
        setDocumentation: (documentationOpen: boolean) => void,
        setModal: (modal: ModalInfo) => void,
        model_id: string,
        selectedColumn: string
    }): JSX.Element => {

    /* Adds a new column onto the end of a sheet, with A, B, C... as the name */
    const addColumn = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        const newColumn = String.fromCharCode(65 + props.sheetJSON.columns.length);
        // Log the new column creation
        window.logger?.track({
            userId: window.user_id,
            event: 'button_column_added_log_event',
            properties: {
                column_header: newColumn
            }
        })
        // TODO: have to update these timestamps, etc to be legit
        props.send({
            'event': 'edit_event',
            'type': 'add_column',
            'sheet_index': props.selectedSheetIndex,
            'id': '123',
            'timestamp': '456',
            'column_header': newColumn
        })
    }

    /* Saves the current file as as an exported analysis */
    const downloadAnalysis = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        window.logger?.track({
            userId: window.user_id,
            event: 'button_download_log_event',
            properties: {}
        })
        // We export using the gridApi.
        window.gridApiMap?.get(props.model_id)?.exportDataAsCsv({
            fileName: 'mito-export'
        });
        props.setModal({type: ModalEnum.Download});
    }

    const openDocumentation = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        // We log the opening of the repeat documentation sidebar
        window.logger?.track({
            userId: window.user_id,
            event: 'button_documentation_log_event',
            properties: {
                stage: 'opened'
            }
        });
        props.setDocumentation(true);
    }

    const openMerge = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        props.setModal({type: ModalEnum.Merge});
    }

    const openGroup = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        props.setModal({type: ModalEnum.Group});
    }

    const openDeleteColumn = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        props.setModal({type: ModalEnum.DeleteColumn, columnHeader: props.selectedColumn});
    }

    const openSave = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);

        props.setModal({type: ModalEnum.SaveAnalysis});
    }

    const openReplay = () => {
        // We turn off editing mode, if it is on
        props.setEditingMode(false, "", -1);
        
        props.setModal({type: ModalEnum.ReplayAnalysis});
    }

    return (
        <div className='mito-toolbar-container'>
            <div className='mito-toolbar-container-left'>
                    <div className='mito-toolbar-item vertical-align-content'>
                        <svg className='mt-p5' width="37" height="30" viewBox="0 0 16 14" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M3.87559 7.30783L5.20063 5.79348C5.78086 5.13036 6.61911 4.74999 7.50024 4.74999L7.54982 4.74999C7.90452 4.74999 8.2447 4.60909 8.49551 4.35827C8.58744 4.26635 8.6995 4.19709 8.82283 4.15598L9.95107 3.77988C10.0721 3.73952 10.1822 3.67153 10.2724 3.58129C10.3982 3.45552 10.6021 3.45552 10.7279 3.58129L12.2894 5.14288C12.5659 5.41934 12.9859 5.40573 13.2501 5.1766L13.2501 5.50001L13.5001 5.50001L13.2501 5.50002C13.2501 5.79001 13.1826 6.07603 13.053 6.33541L12.352 7.73731C12.0198 8.40189 11.4065 8.89073 10.6843 9.07126C10.1561 9.20331 9.66907 9.47751 9.28352 9.8631C9.00842 10.1382 8.67302 10.3455 8.3039 10.4686L7.67731 10.6774C6.58871 11.0403 5.41178 11.0403 4.32317 10.6775L3.50049 10.4032C3.26025 10.3232 3.04194 10.1883 2.86285 10.0092C2.75579 9.90221 2.66414 9.7808 2.59054 9.64851L1.70334 8.05374C2.48732 8.20473 3.32111 7.94153 3.87559 7.30783Z" fill="#343434" fillOpacity="0.5" stroke="#343434" strokeWidth="0.5"/>
                            <path d="M4.64358 9.40301C3.1078 9.0887 -0.290268 8.51438 1.51538 4C2.00277 3.02543 4.25457 2.2291 7.34397 1.06467C7.4569 1.0221 7.57722 1 7.69791 1H9.01538H10.7793C10.9788 1 11.1738 1.05969 11.3391 1.17139L12.2896 1.81355C12.4687 1.93458 12.6038 2.11041 12.6746 2.31468L13.0236 3.32153C13.0644 3.43947 13.0817 3.56392 13.0898 3.68847C13.1095 3.99078 13.1736 4.40493 13.0913 4.97012C12.9842 5.70575 11.7756 6.71418 11.0529 6.88856C10.464 7.03069 9.68653 7.22013 8.68654 7.46977C8.60721 7.48957 8.52382 7.49685 8.44313 7.51008C7.99812 7.58309 7.43142 8.06263 5.43835 9.27491C5.20187 9.41876 4.91476 9.45851 4.64358 9.40301Z" fill="#0081DE" stroke="#343434" strokeWidth="0.5"/>
                            <path d="M3.08838 3.91162L6.5 7.5" stroke="#A3A3A3" strokeWidth="0.25"/>
                            <path d="M5.08838 2.91162L8 6" stroke="#A3A3A3" strokeWidth="0.25"/>
                            <path d="M7.5 2L10.5 5.50001" stroke="#A3A3A3" strokeWidth="0.25"/>
                            <path d="M3 5.49997L9.8638 1.88307" stroke="#A3A3A3" strokeWidth="0.25"/>
                            <path d="M3.50013 7.49997L10.8976 3.3306" stroke="#A3A3A3" strokeWidth="0.25"/>
                        </svg>
                    </div>

                    <button className='mito-toolbar-item vertical-align-content' onClick={addColumn}>
                        <svg width="22" height="30" viewBox="0 0 8 12" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M6.45459 1V2.81818" stroke="#343434" strokeWidth="0.7" strokeLinecap="round"/>
                            <path d="M7.36365 1.90909L5.54547 1.90909" stroke="#343434" strokeWidth="0.7" strokeLinecap="round"/>
                            <path d="M6.45455 4.18182V6.90909V10.5455C6.45455 10.7965 6.25104 11 6 11H1.45455C1.20351 11 1 10.7965 1 10.5455V1.45455C1 1.20351 1.20351 1 1.45455 1H4.8961" stroke="#343434" strokeWidth="0.7"/>
                            <rect x="1" y="4.63635" width="5.45455" height="3.63636" fill="#343434" fillOpacity="0.19"/>
                        </svg>
                        <Tooltip tooltip={"Add Column"}/>
                    </button>
                    <button className='mito-toolbar-item vertical-align-content' onClick={openDeleteColumn}>
                        <svg width="20" height="28" viewBox="0 0 6 9" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M4.57475 8.65H0.922433C0.86766 8.65 0.822173 8.60773 0.818167 8.5531L0.384834 2.64402C0.380391 2.58343 0.428349 2.53182 0.489099 2.53182H4.96869C5.02916 2.53182 5.07702 2.58298 5.073 2.64332L4.67906 8.55241C4.6754 8.60733 4.62979 8.65 4.57475 8.65Z" stroke="#343434" strokeWidth="0.7"/>
                            <path d="M1.25 2.41209V1.5V1H4.25V2.5" stroke="#343434" strokeWidth="0.7" strokeLinecap="round" strokeLinejoin="round"/>
                            <path d="M2 4L1.99993 7.00001" stroke="#343434" strokeWidth="0.7" strokeLinecap="round" strokeLinejoin="round"/>
                            <path d="M3.5 4L3.49993 7.00001" stroke="#343434" strokeWidth="0.7" strokeLinecap="round" strokeLinejoin="round"/>
                        </svg>
                        <Tooltip tooltip={"Delete Column"}/>
                    </button>
                    <div className="vertical-line mt-1"></div>
                    <button className='mito-toolbar-item' onClick={openGroup}>
                    <svg width="30" height="30" viewBox="0 0 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <rect x="1.25" y="8.25" width="5.5" height="5.5" rx="0.75" stroke="#343434" strokeWidth="0.5"/>
                        <rect x="1.25" y="1.25" width="5.5" height="5.5" rx="0.75" stroke="#343434" strokeWidth="0.5"/>
                        <rect x="8.25" y="8.25" width="5.5" height="5.5" rx="0.75" stroke="#343434" strokeWidth="0.5"/>
                        <rect x="8.25" y="1.25" width="5.5" height="5.5" rx="0.75" stroke="#343434" strokeWidth="0.5"/>
                        <circle cx="3" cy="3" r="1" fill="#343434"/>
                        <circle cx="5" cy="5" r="1" fill="#343434"/>
                        <path d="M9.49994 2.49992L9.49992 5.5M12.5 2.5L12.4999 5.50008M10.9999 2.50014L10.9999 5.50022" stroke="#343434" strokeWidth="0.5"/>
                        <path d="M5.63898 9.5L2.32331 9.5M5.63901 12.3181L3.97868 12.3182L2.31834 12.3183M5.63898 10.8809L2.31834 10.8809" stroke="#343434" strokeWidth="0.5"/>
                    </svg>

                        <Tooltip tooltip={"Group"}/>
                    </button>
                    <button className='mito-toolbar-item' onClick={openMerge}>
                        <svg width="40" height="30" viewBox="0 0 23 13" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M14.705 6.5C14.705 9.83244 11.5513 12.625 7.54 12.625C3.52871 12.625 0.375 9.83244 0.375 6.5C0.375 3.16756 3.52871 0.375 7.54 0.375C11.5513 0.375 14.705 3.16756 14.705 6.5Z" fill="#C8C8C8" stroke="#343434" strokeWidth="0.75"/>
                            <path d="M21.9845 6.5C21.9845 9.83244 18.8308 12.625 14.8195 12.625C10.8083 12.625 7.65454 9.83244 7.65454 6.5C7.65454 3.16756 10.8083 0.375 14.8195 0.375C18.8308 0.375 21.9845 3.16756 21.9845 6.5Z" stroke="#343434" strokeWidth="0.75"/>
                        </svg>
                        <Tooltip tooltip={"Merge"}/>
                    </button>
                    <div className="vertical-line mt-1"></div>
                    <button className='mito-toolbar-item' onClick={openSave}>
                        <svg width="30" height="30" viewBox="0 0 10 11" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M0.375 2C0.375 1.10254 1.10254 0.375 2 0.375H5.40054C5.78087 0.375 6.14914 0.5084 6.44124 0.75197L9.0407 2.91958C9.41095 3.22833 9.625 3.68553 9.625 4.16761V9C9.625 9.89746 8.89746 10.625 8 10.625H2C1.10254 10.625 0.375 9.89746 0.375 9V2Z" stroke="#343434" strokeWidth="0.75"/>
                            <rect x="2.125" y="6.0498" width="5.875" height="0.75" fill="#343434"/>
                            <rect x="4.375" y="2.8877" width="2.8875" height="0.75" transform="rotate(-90 4.375 2.8877)" fill="#343434"/>
                            <rect x="2.125" y="8.1123" width="5.875" height="0.75" fill="#343434"/>
                        </svg>
                        <Tooltip tooltip={"Save"}/>
                    </button>
                    <button className='mito-toolbar-item' onClick={openReplay}>
                        <svg width="30" height="30" viewBox="0 0 12 11" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M0.666825 7.72288C0.526284 7.90672 0.561391 8.16969 0.745239 8.31024C0.929087 8.45078 1.19206 8.41567 1.3326 8.23182L0.666825 7.72288ZM2.42647 6.11094L2.64408 5.75286C2.46107 5.64165 2.22365 5.68633 2.09359 5.85647L2.42647 6.11094ZM4.34197 7.7653C4.53973 7.88548 4.79747 7.82259 4.91765 7.62483C5.03783 7.42707 4.97493 7.16933 4.77717 7.04915L4.34197 7.7653ZM1.3326 8.23182L2.75936 6.36541L2.09359 5.85647L0.666825 7.72288L1.3326 8.23182ZM2.20887 6.46901L4.34197 7.7653L4.77717 7.04915L2.64408 5.75286L2.20887 6.46901Z" fill="#343434"/>
                            <path d="M10.2174 5.42936C10.2174 7.61387 8.40507 9.38477 6.16938 9.38477C4.35681 9.38477 2.82247 8.22073 2.30664 6.61598" stroke="#343434" strokeWidth="0.838021"/>
                            <path d="M11.6799 2.73806C11.8204 2.55421 11.7853 2.29124 11.6014 2.1507C11.4176 2.01016 11.1546 2.04527 11.0141 2.22912L11.6799 2.73806ZM9.92021 4.35L9.7026 4.70808C9.88561 4.81929 10.123 4.77461 10.2531 4.60447L9.92021 4.35ZM8.00471 2.69563C7.80695 2.57546 7.54921 2.63835 7.42903 2.83611C7.30885 3.03387 7.37175 3.29161 7.56951 3.41179L8.00471 2.69563ZM11.0141 2.22912L9.58732 4.09553L10.2531 4.60447L11.6799 2.73806L11.0141 2.22912ZM10.1378 3.99192L8.00471 2.69563L7.56951 3.41179L9.7026 4.70808L10.1378 3.99192Z" fill="#343434"/>
                            <path d="M2.12923 5.03157C2.12923 2.84707 3.94161 1.07617 6.1773 1.07617C7.98987 1.07617 9.52421 2.2402 10.04 3.84495" stroke="#343434" strokeWidth="0.838021"/>
                        </svg>
                        <Tooltip tooltip={"Repeat Saved Analysis"}/>
                    </button>
                    <button className='mito-toolbar-item vertical-align-content' onClick={downloadAnalysis}>
                        <svg width="22" height="25" viewBox="0 0 8 9" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M0.899994 5.89999V6.95V8H7.20001V5.89999" stroke="#343434" strokeWidth="0.7" strokeLinecap="round" strokeLinejoin="round"/>
                            <path d="M4.05923 5.39774V0.999997" stroke="#343434" strokeWidth="0.7" strokeLinecap="round"/>
                            <path d="M6.51079 3.88084C6.64455 3.74129 6.63986 3.51974 6.50031 3.38598C6.36077 3.25221 6.13921 3.2569 6.00545 3.39645L6.51079 3.88084ZM4.0905 5.90001L3.8413 6.14577C3.90768 6.21308 3.99846 6.25067 4.09299 6.25C4.18752 6.24933 4.27776 6.21045 4.34317 6.14221L4.0905 5.90001ZM2.10958 3.39288C1.97385 3.25525 1.75225 3.25371 1.61462 3.38944C1.47699 3.52517 1.47545 3.74677 1.61118 3.8844L2.10958 3.39288ZM6.00545 3.39645L3.83783 5.65782L4.34317 6.14221L6.51079 3.88084L6.00545 3.39645ZM4.33971 5.65425L2.10958 3.39288L1.61118 3.8844L3.8413 6.14577L4.33971 5.65425Z" fill="#343434"/>
                        </svg>
                        <Tooltip tooltip={"Download Sheet"}/>
                    </button>
                    {/* add className mito-toolbar-item to a div below to add another toolbar item! */}
            </div>
            <div className='mito-toolbar-container-right mr-5'>
                <button className='mito-toolbar-item' onClick={openDocumentation}>
                    <svg width="25" height="25" viewBox="0 0 14 14" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <circle cx="7" cy="7" r="6.51" stroke="#404040" strokeWidth="0.98"/>
                        <path d="M7.27173 8.43865C7.2624 8.34531 7.2624 8.30798 7.2624 8.26131C7.2624 7.89731 7.38373 7.56131 7.67307 7.36531L8.1024 7.07598C8.64373 6.71198 9.0544 6.19865 9.0544 5.45198C9.0544 4.49998 8.31707 3.57598 7.0104 3.57598C5.57307 3.57598 4.94773 4.63065 4.94773 5.48931C4.94773 5.65731 4.9664 5.80665 5.00373 5.93731L5.90907 6.04931C5.87173 5.94665 5.84373 5.75065 5.84373 5.59198C5.84373 5.00398 6.1984 4.39731 7.0104 4.39731C7.75707 4.39731 8.12107 4.91065 8.12107 5.46131C8.12107 5.82531 7.94373 6.16131 7.6264 6.37598L7.21573 6.65598C6.66507 7.02931 6.44107 7.49598 6.44107 8.11198C6.44107 8.23331 6.44107 8.32665 6.4504 8.43865H7.27173ZM6.24507 9.77331C6.24507 10.1093 6.51573 10.38 6.85173 10.38C7.18773 10.38 7.46773 10.1093 7.46773 9.77331C7.46773 9.43731 7.18773 9.15731 6.85173 9.15731C6.51573 9.15731 6.24507 9.43731 6.24507 9.77331Z" fill="#343434"/>
                    </svg>
                    <Tooltip tooltip={"Documentation"}/>
                </button>
            </div>
        </div>
    );
};

export default MitoToolbar;