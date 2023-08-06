// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import React from 'react';

// import css
import "../../css/sheet-tab.css"

type SheetTabProps = {
    sheetName: string;
    sheetIndex: number;
    selectedSheetIndex: number;
    setSelectedSheetIndex: (newIndex: number) => void;
};


export default function SheetTab(props : SheetTabProps) : JSX.Element {

    const sheetName = props.sheetName ? props.sheetName : "sheet1";

    return (
        <div className="tab" onClick={() => {props.setSelectedSheetIndex(props.sheetIndex)}}>
            <div>
                <p>
                    {sheetName}
                </p>
                {
                    props.selectedSheetIndex == props.sheetIndex &&
                    <hr className="selected-tab-indicator"></hr>
                }
                
            </div>  
        </div>
    );
}
