// Copyright (c) Mito
// Distributed under the terms of the Modified BSD License.

import {
  DOMWidgetModel,
  DOMWidgetView,
  ISerializers,
  WidgetView,
} from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';

// Import the CSS
import '../css/widget.css';

// React
import React from 'react';
import ReactDOM from 'react-dom';

// Components
import Mito, { ColumnSpreadsheetCodeJSON, SheetColumnFiltersArray, ColumnTypeJSONArray } from './components/Mito';

// Logging
import Analytics from 'analytics-node';
import { GridApi } from 'ag-grid-community';

export class ExampleModel extends DOMWidgetModel {

  // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
  defaults() {
    return {
      ...super.defaults(),
      _model_name: ExampleModel.model_name,
      _model_module: ExampleModel.model_module,
      _model_module_version: ExampleModel.model_module_version,
      _view_name: ExampleModel.view_name,
      _view_module: ExampleModel.view_module,
      _view_module_version: ExampleModel.view_module_version,
      df_json: '',
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // Add any extra serializers here
  };

  static model_name = 'ExampleModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'ExampleView'; // Set to null if no view
  static view_module = MODULE_NAME; // Set to null if no view
  static view_module_version = MODULE_VERSION;
}

// We save a Mito component in the global scope, so we
// can set the state from outside the react component
declare global {
  interface Window { 
    mitoMap:  Map<string, Mito> | undefined;
    gridApiMap: Map<string, GridApi> | undefined;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    commands: any;
    logger: Analytics | undefined;
    user_id: string;
  }
}

export interface SheetJSON {
  columns: (string|number)[];
  index: string[];
  data: string[][];
}

export interface CodeJSON {
  imports: string;
  code: string[];
}

export interface ErrorJSON {
  event: string;
  type: string;
  header: string;
  to_fix: string;
}

import { ModalEnum } from "./components/Mito";

export class ExampleView extends DOMWidgetView {
  /*
    We override the DOMWidgetView constructor, so that we can
    create a logging instance for this view. 
  */
  initialize(parameters : WidgetView.InitializeParameters) : void {
    super.initialize(parameters);

    // We get the user id from the client side
    window.user_id = this.model.get('user_id');
    // Write key taken from segment.com
    window.logger = new Analytics('L4FqIZ3qB4C2FBitK4gUn073vv3lyWXm');
    // Identify the user
    window.logger.identify({userId: window.user_id});
  }

  /* 
    We override the sending message utilities, so that we can log all
    outgoing messages
  */
  send(msg: Record<string, unknown>) : void{
    // Log the out-going message
    window.logger?.track({
      userId: window.user_id,
      event: 'js_sent_msg_log_event',
      properties: {
        event: msg
      }
    })
    super.send(msg);
  }

  render() : void {  
    // Capture the send, to pass to the component
    const send = (msg: Record<string, unknown>) => {
      this.send(msg);
    }

    // TODO: there is a memory leak, in the case where
    // we rerender the component (e.g. we run the mito.sheet)
    // cell again. We need to clean up the component somehow!
    const model_id = this.model.model_id;

    ReactDOM.render(
      <Mito 
        dfNames={this.getDfNames()}
        sheetJSONArray={this.getSheetJSONArray()}
        columnSpreadsheetCodeJSONArray={this.getColumnSpreadsheetCodeJSONArray()}
        savedAnalysisNames={this.getSavedAnalysisNames()}
        columnFiltersArray={this.getColumnFilters()}
        columnTypeJSONArray={this.getColumnTypeJSONArray()}
        send={send}
        model_id={model_id}
        ref={(Mito : Mito) => { 
          if (window.mitoMap === undefined) {
            window.mitoMap = new Map();
          }
          window.mitoMap.set(model_id, Mito);
        }}
        />,
      this.el
    )
    this.model.on('msg:custom', this.handleMessage, this);

    // TODO: make both of these only on the first render, not all of them... doh

    // Get df name from code block, and pass it to both the frontend and the backend
    window.commands?.execute('get-df-names').then((dfNames : string[]) => {
      // set the data frame name in the model state
      this.send({
        'event': 'update_event',
        'type': 'df_names_update',
        'df_names': dfNames
      })
      // set the data frame name in the widget
      window.mitoMap?.get(this.model.model_id)?.setState({dfNames: dfNames});
    });

    // Get any previous analysis and send it back to the model!
    window.commands?.execute('read-existing-analysis').then((analysisName : string | undefined) => {
      // If there is no previous analysis, we just ignore this step
      if (!analysisName) return;
      // And send it to the backend model
      this.send({
        'event': 'update_event',
        'type': 'use_existing_analysis_update',
        'analysis_name': analysisName
      })
      // We let the resulting update event update the backend!
    });
    
    // Log that this view was rendered
    window.logger?.track({
      userId: window.user_id,
      event: 'sheet_view_creation_log_event',
      properties: {}
    });
  }

  getSheetJSONArray(): SheetJSON[] {
    const sheetJSONArray: SheetJSON[] = [];

    try {
      const modelSheetJSONArray = JSON.parse(this.model.get('sheet_json'));
      sheetJSONArray.push(...modelSheetJSONArray);
    } catch (e) {
      // Suppress error
    }

    return sheetJSONArray;
  }

  getColumnTypeJSONArray(): ColumnTypeJSONArray {
    const columnTypeJSONArray: ColumnTypeJSONArray = [];

    try {
      const modelColumnTypeJSONArray = JSON.parse(this.model.get('column_type_json'));
      columnTypeJSONArray.push(...modelColumnTypeJSONArray);
    } catch (e) {
      // Suppress error
    }

    return columnTypeJSONArray;
  }

  getSavedAnalysisNames(): string[] {
    const savedAnalysisNames: string[] = [];

    try {
      const savedAnalysisNamesJSON = JSON.parse(this.model.get('saved_analysis_names_json'));
      savedAnalysisNames.push(...savedAnalysisNamesJSON);
    } catch (e) {
      // Suppress error
    }

    return savedAnalysisNames;
  }

  getColumnSpreadsheetCodeJSONArray() : ColumnSpreadsheetCodeJSON[] {
    return JSON.parse(this.model.get('column_spreadsheet_code_json'));
  }

  getDfNames(): string[] {
    const dfNames : string[]= [];

    const unparsedDfNames = this.model.get('df_names_json');
    try {
      dfNames.push(...JSON.parse(unparsedDfNames)['df_names']);

      // And then we extend it to the length of the number of sheets,
      // as the dfNames sometimes aren't pulled correctly!
      const modelSheetJSONArray = this.getSheetJSONArray();
      for (let i = dfNames.length; i < modelSheetJSONArray.length; i++) {
        dfNames.push(`df${i + 1}`);
      }
    } catch (e) {
      // Suppress error
    }
    return dfNames;
  }

  getCodeJSON(): CodeJSON {
    const codeJSON: CodeJSON = {
      imports: '# No imports',
      code: ['# No code has been written yet!', 'pass']
    };

    const unparsedCodeJSON = this.model.get('code_json');
    try {
      codeJSON['imports'] = JSON.parse(unparsedCodeJSON)['imports'];
      codeJSON['code'] = JSON.parse(unparsedCodeJSON)['code'];
    } catch (e) {
      // Suppress error
    }
    return codeJSON;
  }

  getAnalysisName(): string {
    return this.model.get('analysis_name') as string;
  }

  getColumnFilters(): SheetColumnFiltersArray {
    return JSON.parse(this.model.get('column_filters_json'));
  }

  handleMessage(message : any) : void {
    /* 
      This route handles the messages sent from the Python widget
    */
  
    // Log that we received this message
    window.logger?.track({
      userId: window.user_id,
      event: 'js_recv_msg_log_event',
      properties: {
        event: message
      }
    })

    const model_id = this.model.model_id;
    const mito = window.mitoMap?.get(model_id);

    if (mito === undefined) {
      console.error("Error: a message was received for a mito instance that does not exist!")
      return;
    }

    console.log("Got a message, ", message);
    if (message.event === 'update_sheet') {
      console.log("Updating sheet.");
      mito.setState({
        sheetJSONArray: this.getSheetJSONArray(),
        columnSpreadsheetCodeJSONArray: this.getColumnSpreadsheetCodeJSONArray(),
        dfNames: this.getDfNames(),
        savedAnalysisNames: this.getSavedAnalysisNames(),
        columnFiltersArray: this.getColumnFilters(),
        columnTypeJSONArray: this.getColumnTypeJSONArray()
      });
    } else if (message.event === 'update_code') {
      console.log('Updating code.');
      window.commands?.execute('write-code-to-cell', {
        analysisName: this.getAnalysisName(),
        codeJSON: this.getCodeJSON()
      });
    } else if (message.event === 'edit_error') {
      console.log("Updating edit error.");
      mito.setState({
        modalInfo: {type: ModalEnum.Error},
        errorJSON: message
      });
    }
  }
}
