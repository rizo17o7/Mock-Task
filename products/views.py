from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Material, ProductMaterial, Warehouse
from .serializers import ProductSerializer, WarehouseSerializer


class ProductMaterialsAPIView(APIView):
    def get(self, request, product_id, quantity):
        product = Product.objects.get(id=product_id)
        product_materials = ProductMaterial.objects.filter(product=product)

        response_data = {
            "product_name": product.name,
            "product_qty": quantity,
            "product_materials": []
        }

        for pm in product_materials:
            material = pm.material
            required_qty = pm.quantity * quantity

            warehouses = Warehouse.objects.filter(material=material).order_by('id')
            material_data = {
                "material_name": material.name,
                "qty": required_qty,
                "warehouses": []
            }

            for warehouse in warehouses:
                if required_qty <= 0:
                    break
                available_qty = warehouse.remainder
                if available_qty >= required_qty:
                    material_data["warehouses"].append({
                        "warehouse_id": warehouse.id,
                        "qty": required_qty,
                        "price": warehouse.price
                    })
                    required_qty = 0
                else:
                    material_data["warehouses"].append({
                        "warehouse_id": warehouse.id,
                        "qty": available_qty,
                        "price": warehouse.price
                    })
                    required_qty -= available_qty

            if required_qty > 0:
                material_data["warehouses"].append({
                    "warehouse_id": None,
                    "qty": required_qty,
                    "price": None
                })

            response_data["product_materials"].append(material_data)

        return Response(response_data)


class MultipleProductsMaterialsAPIView(APIView):
    def post(self, request):
        products = request.data.get("products", [])
        response_data = []

        for product in products:
            product_id = product["product_id"]
            quantity = product["quantity"]
            view = ProductMaterialsView()
            response = view.get(request, product_id, quantity)
            response_data.append(response.data)

        return Response({"result": response_data})