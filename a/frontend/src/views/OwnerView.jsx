import React, { useState, useEffect } from 'react';
import { Button, Modal, Tabs, Tab } from 'react-bootstrap';
import api from "../api";

// Import principal entity's Table and Form
import OwnerTable from '../components/OwnerTable';
import OwnerForm from '../components/OwnerForm';

// Import related entities' Table and Form

import PetTable from '../components/PetTable';
import PetForm from '../components/PetForm';


const OwnerView = () => {

    // Main data state
    const [mainData, setMainData] = useState([]);

    // States for modals and actions on the main entity
    const [showForm, setShowForm] = useState(false);
    const [currentItem, setCurrentItem] = useState(null); // for editing
    const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
    const [deleteItemId, setDeleteItemId] = useState(null);

    // States for related entities
    const [relatedData, setRelatedData] = useState({});
    const [activeTab, setActiveTab] = useState(null);

    // States and control for related-entity Form modal
    const [showRelatedForm, setShowRelatedForm] = useState(false);
    const [relatedEntity, setRelatedEntity] = useState(null);

    // **Nuevo estado para editar/crear un objeto relacionado**
    const [currentRelatedItem, setCurrentRelatedItem] = useState(null);

    /**
     * Map of related Forms:
     * Assumes each relationship has its own Form component
     * imported above. Adjust names to exactly match your files.
     */
    const relatedFormsMap = {
        
        'Pet': PetForm,
        
    };

    // Dynamically determine which Form to render (based on `relatedEntity`)
    const FormToRender = relatedEntity ? relatedFormsMap[relatedEntity] : null;

    // On mount, fetch main entity data
    useEffect(() => {
        fetchMainData();
    }, []);

    const fetchMainData = () => {
        api.get(`/owners/`)
           .then((response) => setMainData(response.data))
           .catch((err) => console.error('Error fetching main data:', err));
    };

    // =====================
    //  CREATE NEW (forces id=null)
    // =====================
    const handleCreateNew = () => {
        setRelatedData({});       // <--- limpiamos los datos relacionados
        setCurrentItem(null);     // <--- nos aseguramos de limpiar el item
        setShowForm(true);        //      para que el Form reciba id={null}
    };

    // =====================
    //      EDIT
    // =====================
    const handleEdit = (item) => {
        // Al editar, guardamos el item en currentItem
        // para que el Form reciba id={item.id}
        setCurrentItem(item);
        setShowForm(true);

        // Fetch related data for the selected item
        
        api.get(`/owners/${item.id}/pets`)
           .then((response) => {
               setRelatedData((prev) => ({
                   ...prev,
                   'pet': response.data,
               }));
           })
           .catch((err) =>
               console.error('Error fetching related data for Pet:', err)
           );
        
    };

    // =====================
    //      DELETE
    // =====================
    const handleDelete = (id) => {
        setDeleteItemId(id);
        setShowDeleteConfirm(true);
    };

    const confirmDelete = () => {
        api.delete(`/owners/${deleteItemId}`)
           .then(() => {
               console.log('Item deleted');
               setShowDeleteConfirm(false);
               fetchMainData(); // refresh main list
           })
           .catch((err) => console.error('Error deleting item:', err));
    };

    // =====================
    //   SELECT (VIEW RELATED)
    // =====================
    const handleSelect = (item) => {
        setCurrentItem(item);

        
        api.get(`/owners/${item.id}/pets`)
           .then((response) => {
               setRelatedData((prev) => ({
                   ...prev,
                   'pet': response.data,
               }));
           })
           .catch((err) =>
               console.error('Error fetching related data for Pet:', err)
           );
        
    };

    // =====================
    //  CREATE RELATED ENTITY
    // =====================
    const handleAddRelated = (entity) => {
        setCurrentRelatedItem(null);
        setRelatedEntity(entity);
        setShowRelatedForm(true);
    };

  // =====================
  //   EDIT RELATED
  // =====================
  const handleEditRelated = (entity, item) => {
    setCurrentRelatedItem(item);
    setRelatedEntity(entity);
    setShowRelatedForm(true);
  };

  // =====================
  //   DELETE RELATED
  // =====================
  const handleDeleteRelated = (entity, itemId) => {
    api
      .delete(`/${entity.toLowerCase()}s/${itemId}`)
      .then(() => {
        console.log(`Deleted ${entity} id=${itemId}`);
        if (currentItem) {
          api.get(`/owners/${currentItem.id}/${entity.toLowerCase()}s`)
             .then((resp) => {
                setRelatedData((prev) => ({
                    ...prev,
                    [entity.toLowerCase()]: resp.data,
                }));
             })
             .catch((err) => console.error(`Error fetching ${entity} after delete:`, err));
        }
      })
      .catch((err) =>
        console.error(`Error deleting ${entity} with id=${itemId}:`, err)
      );
  };

    // Handle tab changes
    const handleTabChange = (tabKey) => {
        setActiveTab(tabKey);
    };

    // Callback after create/update main entity
    const handleFormSuccess = () => {
        setShowForm(false);
        setCurrentItem(null);
        fetchMainData();
    };

    // Callback after create/update related entity
    const handleRelatedFormSuccess = () => {
        setShowRelatedForm(false);
        setRelatedEntity(null);

        // Optionally, refresh the related data for the current item
        if (currentItem) {
            
            api.get(`/owners/${currentItem.id}/pets`)
               .then((response) => {
                   setRelatedData((prev) => ({
                       ...prev,
                       'pet': response.data,
                   }));
               })
               .catch((err) =>
                   console.error('Error fetching related data for Pet:', err)
               );
            
        }
    };

    return (
        <div>
            <h1>Owner View</h1>

            {/* Main table section */}
            <div className="main-table">
                <OwnerTable
                    data={mainData}
                    onEdit={handleEdit}
                    onDelete={handleDelete}
                    onSelect={handleSelect}
                />

                {/* Bot�n para CREAR una nueva entidad => siempre id=null */}
                <Button className="mb-2" onClick={handleCreateNew}>
                    Add New Owner
                </Button>
            </div>

            {/* Related entities section */}
            <Tabs activeKey={activeTab} onSelect={handleTabChange} className="my-3">
                
                
                <Tab eventKey="pet" title="Pet">
                    <div className="related-table">
                        {relatedData["pet"] ? (
                            <div>
                                <PetTable
                                    data={relatedData["pet"]}
                                    onEdit={(item) => handleEditRelated('Pet', item)}
                                    onDelete={(itemId) => handleDeleteRelated('Pet', itemId)}
                                />
                                <Button
                                    className="mt-2"
                                    variant="success"
                                    onClick={() => handleAddRelated('Pet')}
                                >
                                    Add New Pet
                                </Button>
                            </div>
                        ) : (
                            <p>
                                Select an item from the main table to view related
                                 Pets.
                            </p>
                        )}

                    </div>
                </Tab>
                
                
            </Tabs>

            {/* Modal for main entity Form */}
            <Modal show={showForm} onHide={() => setShowForm(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>
                        {currentItem ? 'Edit' : 'Create'} Owner
                    </Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    <OwnerForm
                        id={currentItem?.id || null}
                        onSuccess={handleFormSuccess}
                    />
                </Modal.Body>
            </Modal>

            {/* Modal for related entity Form */}
            <Modal show={showRelatedForm} onHide={() => setShowRelatedForm(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>{currentRelatedItem ? 'Edit' : 'Create'} New {relatedEntity}</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {FormToRender && React.createElement(FormToRender, {
                        id: currentRelatedItem?.id || null, // for editing
                        onSuccess: handleRelatedFormSuccess,
                        // Pass the parent info so the Form can do a nested POST
                        parent: 'owner',
                        parentId: currentItem?.id
                    })}
                </Modal.Body>
            </Modal>

            {/* Modal to confirm deletion */}
            <Modal
                show={showDeleteConfirm}
                onHide={() => setShowDeleteConfirm(false)}
            >
                <Modal.Header closeButton>
                    <Modal.Title>Confirm Delete</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    Are you sure you want to delete this item?
                </Modal.Body>
                <Modal.Footer>
                    <Button
                        variant="secondary"
                        onClick={() => setShowDeleteConfirm(false)}
                    >
                        Cancel
                    </Button>
                    <Button variant="danger" onClick={confirmDelete}>
                        Delete
                    </Button>
                </Modal.Footer>
            </Modal>
        </div>
    );
};

export default OwnerView;