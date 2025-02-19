import React, { useState, useEffect } from 'react';
import api from "../api";

const OwnerTable = ({ onEdit, onDelete, onSelect, id, data: passedData }) => {
    const [data, setData] = useState(passedData ? passedData : []);
    // Para List, cargamos los datos si no vienen por props
    const [loading, setLoading] = useState(!passedData);
    const [error, setError] = useState(null);

    const API_BASE_URL = `${process.env.REACT_APP_API_HOST}:${process.env.REACT_APP_API_PORT}`;

    useEffect(() => {
        // Solo hacemos la llamada si no tenemos "passedData"
        if (!passedData) {
            api.get(`/owners`)
                .then(response => {
                    setData(response.data);
                    setLoading(false);
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                    setError(error);
                    setLoading(false);
                });
        }
        else{
            setData(passedData)
        }
    }, [id, passedData]);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;

    // Campos que se renderizarán en la tabla (puedes ajustarlo según tu lógica)
    let fields = [{"name": "first_name", "type": "text"}, {"name": "last_name", "type": "text"}];

    return (
        <table className="table">
            <thead>
                <tr>
                    <th>ID</th>
                    {fields.map((field) => (
                        <th key={field.name}>{field.name}</th>
                    ))}
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {data.map(item => (
                    <tr
                        key={item.id}
                        onClick={() => onSelect && onSelect(item)}
                        className="clickable-row"
                    >
                        <td>{item.id}</td>
                        {fields.map((field) => (
                            <td key={field.name}>{item[field.name]}</td>
                        ))}
                        <td>
                            {onEdit && (
                                <button
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        onEdit(item);
                                    }}
                                >
                                    Edit
                                </button>
                            )}
                            {onDelete && (
                                <button
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        onDelete(item.id);
                                    }}
                                >
                                    Delete
                                </button>
                            )}
                        </td>
                    </tr>
                ))}
            </tbody>
        </table>
    );
};

export default OwnerTable;