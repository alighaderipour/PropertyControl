// frontend/src/stores/properties.js
import { defineStore } from "pinia";
import { ref } from "vue";
import { useAuthStore } from "@/stores/auth"; // Make sure this path is correct

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

// API helper function

export async function apiRequest(url, method = "GET", data = null) {
  const token = localStorage.getItem("access_token");

  const headers = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
  };

  const config = {
    method,
    headers,
  };

  if (data) {
    config.body = JSON.stringify(data);
  }

  const response = await fetch(`http://localhost:8000${url}`, config);

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return await response.json();
}

async function transferProperty(propertyId, departmentId) {
  const payload = { department: departmentId };

  const response = await apiRequest(
    `/api/properties/${propertyId}/transfer/`,
    "PUT",
    payload
  );
  return response;
}



export const usePropertiesStore = defineStore("properties", () => {
  // At the top-level inside defineStore:
  const count = ref(0);
  const next = ref(null);
  const previous = ref(null);
  const error = ref(null);

  // State
  const properties = ref([]);
  const departments = ref([]);
  const categories = ref([]);
  const loading = ref(false);

  // Actions
 const fetchProperties = async (params = {}) => {
    loading.value = true;
    error.value = null;
    try {
      const queryParams = new URLSearchParams(params);
      const data = await apiRequest(`/api/properties/?${queryParams}`);
      properties.value = data.results || data;
      count.value = data.count ?? properties.value.length;
      next.value = data.next;
      previous.value = data.previous;
      return data;
    } catch (err) {
      error.value = "Error fetching properties";
      throw err;
    } finally {
      loading.value = false;
    }
  };


  const getProperty = async (id) => {
    try {
      const data = await apiRequest(`/api/properties/${id}/`);
      return data;
    } catch (error) {
      console.error("Error fetching property:", error);
      throw error;
    }
  };

const addProperty = async (propertyData) => {
  try {
    // ✅ CORRECT: method string, then data
    const data = await apiRequest("/api/properties/", "POST", propertyData);
    properties.value.push(data);
    return data;
  } catch (error) {
    console.error("Error adding property:", error);
    throw error;
  }
};


const updateProperty = async (id, propertyData) => {
  try {
    const data = await apiRequest(`/api/properties/${id}/`, "PATCH", propertyData);
    const index = properties.value.findIndex((p) => p.id === parseInt(id));
    if (index !== -1) properties.value[index] = data;
    return data;
  } catch (error) {
    console.error("Error updating property:", error);
    throw error;
  }
};


const deleteProperty = async (id) => {
  try {
    await apiRequest(`/api/properties/${id}/`, "DELETE");
    properties.value = properties.value.filter((p) => p.id !== parseInt(id));
    return true;
  } catch (error) {
    console.error("Error deleting property:", error);
    throw error;
  }
};

  const fetchDepartments = async () => {
    try {
      const data = await apiRequest("/api/departments/");
      departments.value = data.results || data;
      return data;
    } catch (error) {
      console.error("Error fetching departments:", error);
      throw error;
    }
  };

  const fetchCategories = async () => {
    try {
      const data = await apiRequest("/api/categories/");
      categories.value = data.results || data;
      return data;
    } catch (error) {
      console.error("Error fetching categories:", error);
      throw error;
    }
  };

  const getPropertyById = (id) => {
    return properties.value.find((p) => p.id === parseInt(id));
  };

  return {
  properties, departments, categories, loading,
  count, next, previous, error,       // <== add these
  fetchProperties, getProperty, addProperty, updateProperty, deleteProperty,
  fetchDepartments, fetchCategories, getPropertyById,
  transferProperty
};

  
});
