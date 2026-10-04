"""Deterministic service catalogue and validation engine."""

import json
import os
from typing import Optional
from pydantic import BaseModel

class ServiceValidationResult(BaseModel):
    valid: bool
    service_category: Optional[str] = None
    service: Optional[str] = None
    specialization: Optional[str] = None
    reason: str

class ServiceCatalogue:
    def __init__(self, data_path: Optional[str] = None):
        if data_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            data_path = os.path.join(base_dir, "seed", "services.json")
        
        with open(data_path, "r", encoding="utf-8") as f:
            self._data = json.load(f)
            
        self._build_indexes()
        
    def _build_indexes(self):
        self._categories = {}
        self._services = {}
        self._service_names = {}
        
        for category_data in self._data:
            cat_name = category_data["category"]
            norm_cat = self._normalize(cat_name)
            self._categories[norm_cat] = cat_name
            
            for service in category_data.get("services", []):
                srv_id = service["id"]
                srv_name = service["name"]
                norm_srv = self._normalize(srv_name)
                norm_id = self._normalize(srv_id)
                
                service_info = {
                    "category": cat_name,
                    "service_data": service,
                    "specializations": {self._normalize(issue): issue for issue in service.get("common_issues", [])}
                }
                
                self._services[srv_id] = service_info
                
                self._service_names[norm_srv] = srv_id
                self._service_names[norm_id] = srv_id

    def _normalize(self, text: str) -> str:
        """Safe normalization for service names and categories."""
        if not text:
            return ""
        normalized = text.lower().replace("-", " ").replace("_", " ")
        return " ".join(normalized.split())

    def validate(self, service_category: Optional[str] = None, service: Optional[str] = None, specialization: Optional[str] = None) -> ServiceValidationResult:
        if not service_category and not service and not specialization:
            return ServiceValidationResult(valid=False, reason="No service details provided.")
            
        validated_category = None
        validated_service = None
        validated_specialization = None
        
        if service:
            norm_service = self._normalize(service)
            srv_id = self._service_names.get(norm_service)
            if not srv_id:
                return ServiceValidationResult(valid=False, reason=f"Unknown service: {service}")
            
            validated_service = srv_id
            service_info = self._services[srv_id]
            
            if service_category:
                norm_cat = self._normalize(service_category)
                cat_name = self._categories.get(norm_cat)
                
                if cat_name != service_info["category"]:
                    validated_category = service_info["category"]
                else:
                    validated_category = cat_name
            else:
                validated_category = service_info["category"]
                
            if specialization:
                norm_spec = self._normalize(specialization)
                specs = service_info["specializations"]
                
                if norm_spec in specs:
                    validated_specialization = specs[norm_spec]
                else:
                    return ServiceValidationResult(
                        valid=False,
                        service_category=validated_category,
                        service=validated_service,
                        reason=f"Unsupported specialization '{specialization}'"
                    )
                    
        elif service_category:
            norm_cat = self._normalize(service_category)
            if norm_cat not in self._categories:
                return ServiceValidationResult(valid=False, reason=f"Unknown service category: {service_category}")
            validated_category = self._categories[norm_cat]
            if specialization:
                 return ServiceValidationResult(valid=False, reason="Cannot validate specialization without a specific service.")
                 
        else:
            return ServiceValidationResult(valid=False, reason="Service must be provided to validate specialization.")

        return ServiceValidationResult(
            valid=True,
            service_category=validated_category,
            service=validated_service,
            specialization=validated_specialization,
            reason="Valid service requirement"
        )
