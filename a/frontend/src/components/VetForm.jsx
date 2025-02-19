import React, { useState, useEffect } from 'react';
import api from "../api";

const VetForm = ({
    id,
    data: passedData,
    onSuccess
}) => {
    const [formData, setFormData] = useState(passedData || {});
    const [loading, setLoading] = useState(!passedData && !!id);
    const [error, setError] = useState(null);
    const [dropdownOptions, setDropdownOptions] = useState({}); // Store options for all relationships

    const API_BASE_URL = `${process.env.REACT_APP_API_HOST}:${process.env.REACT_APP_API_PORT}`;

    useEffect(() => {
        if (!passedData && id) {
            api.get(`/vets/${id}`)
               .then((response) => {
                   setFormData(response.data);
                   setLoading(false);
               })
               .catch((error) => {
                   console.error('Error fetching form data:', error);
                   setError(error);
                   setLoading(false);
               });
        }
    }, [id, passedData]);

    useEffect(() => {
        // Load dropdown options for all relationships
        const fetchDropdownOptions = async () => {
            const options = {};

            for (const rel of [{"target": "Visit", "type": "NestedTableComponent"}]) {
                if (rel.type === 'ParentReferenceComponent') {
                    try {
                        const response = await api.get(`/${rel.target.toLowerCase()}s/`);
                        options[rel.target] = response.data;
                    } catch (error) {
                        console.error(`Error fetching options for ${rel.target}:`, error);
                    }
                }
            }

            setDropdownOptions(options);
        };

        fetchDropdownOptions();
    }, []);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({
            ...prev,
            [name]: value,
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();

        const method = id ? 'put' : 'post';

        let url = `/vets/`;
        const payload = { ...formData };

        if (id) {
            url = `/vets/${id}`;
        }

        api[method](url, payload)
            .then((response) => {
                console.log('Data saved successfully:', response.data);
                if (onSuccess) {
                    onSuccess(response.data);
                }
            })
            .catch((error) => {
                console.error('Error saving data:', error);
                setError(error);
            });
    };

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;

    const fields = [{"name": "first_name", "type": "text"}, {"name": "last_name", "type": "text"}];
    const relationships = [{"target": "Visit", "type": "NestedTableComponent"}];

    return (
        <form onSubmit={handleSubmit}>
            {fields.map((field) => (
                <div key={field.name}>
                    <label htmlFor={field.name}>{field.name}</label>
                    <input
                        type={field.type}
                        id={field.name}
                        name={field.name}
                        value={formData[field.name] || ''}
                        onChange={handleInputChange}
                    />
                </div>
            ))}

            {relationships.map((rel) => (
                rel.type === 'ParentReferenceComponent' && (
                    <div key={rel.target}>
                        <label htmlFor={`${rel.target}Dropdown`}>Select {rel.target}</label>
                        <select
                            id={`${rel.target}Dropdown`}
                            name={`${rel.target.toLowerCase()}_id`}
                            value={formData[`${rel.target.toLowerCase()}_id`] || ''}
                            onChange={handleInputChange}
                        >
                            <option value="">Select a {rel.target}</option>
                            {(dropdownOptions[rel.target] || []).map((option) => (
                                <option key={option.id} value={option.id}>
                                    {[option.id, ...Object.entries(option)
                                        .filter(([key, value]) => typeof value === 'string')
                                        .map(([key, value]) => value)
                                    ].join(' - ') || option.id}
                                </option>
                            ))}
                        </select>
                    </div>
                )
            ))}

            <button type="submit">{id ? 'Update' : 'Create'}</button>
        </form>
    );
};

export default VetForm;