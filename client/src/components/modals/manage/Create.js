/* Copyright 2018 Contributors to Hyperledger Sawtooth

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
----------------------------------------------------------------------------- */


import React, { Component } from 'react';
import { Button, Form, Header, Icon, Modal } from 'semantic-ui-react';
import PropTypes from 'prop-types';
import './Create.css';


/**
 *
 * @class         Create
 * @description   Create role modal
 *
 */
export default class Create extends Component {

  static propTypes = {
    submit: PropTypes.func,
  };


  state = { name: '', validName: null, open: false };


  /**
   * Handle form change event
   * @param {object} event Event passed by Semantic UI
   * @param {string} name  Name of form element derived from
   *                       HTML attribute 'name'
   * @param {string} value Value of form field
   */
  handleChange = (event, { name, value }) => {
    this.setState({ [name]: value });
    this.validate(name, value);
  }


  handleOpen = () => this.setState({ open: true });
  handleClose = () => this.setState({
    open: false,
    validName: null,
    name: '',
  });


  handleSubmit = () => {
    const { submit } = this.props;
    const { name } = this.state;

    this.handleClose();
    submit(name);
  }


  /**
   * Validate create role form
   * @param {string} name  Name of form element derived from
   *                       HTML attribute 'name'
   * @param {string} value Value of form field
   */
  validate = (name, value) => {
    name === 'name' &&
      this.setState({ validName: value.length > 4 });
  }


  /**
   * Render entrypoint
   * @returns {JSX}
   */
  render () {
    const { open, validName } = this.state;

    return (
      <Modal
        trigger={<Button icon='add' onClick={this.handleOpen}/>}
        basic
        dimmer='inverted'
        size='mini'
        open={open}
        onClose={this.handleClose}>
        <Header icon='add' content='Create New Role' />
        <Modal.Content>
          <p>Create a new role.</p>
          <Form>
            <Form.Input
              autoFocus
              error={validName === false}
              name='name'
              placeholder='Name'
              onChange={this.handleChange}/>
          </Form>
        </Modal.Content>
        <Modal.Actions>
          <Button basic color='red' onClick={this.handleClose}>
            <Icon name='remove'/> Close
          </Button>
          <Button
            color='green'
            disabled={!validName}
            onClick={this.handleSubmit}>
            <Icon name='add'/> Create
          </Button>
        </Modal.Actions>
      </Modal>
    );
  }

}
