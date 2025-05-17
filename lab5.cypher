// Покупці
CREATE (c1:Customer {id: "cust1", name: "Olena"})
CREATE (c2:Customer {id: "cust2", name: "Ivan"})
CREATE (c3:Customer {id: "cust3", name: "Nina"})
CREATE (c4:Customer {id: "cust4", name: "Andrii"})
CREATE (c5:Customer {id: "cust5", name: "Marta"})

// Товари
CREATE (i1:Item {id: "item1", name: "Laptop", price: 1000})
CREATE (i2:Item {id: "item2", name: "Mouse", price: 50})
CREATE (i3:Item {id: "item3", name: "Keyboard", price: 80})
CREATE (i4:Item {id: "item4", name: "Monitor", price: 300})
CREATE (i5:Item {id: "item5", name: "Desk", price: 200})
CREATE (i6:Item {id: "item6", name: "Chair", price: 150})

// Категорії
CREATE (cat1:Category {name: "Electronics"})
CREATE (cat2:Category {name: "Furniture"})

// Прив'язка товарів до категорій
CREATE (i1)-[:BELONGS_TO]->(cat1)
CREATE (i2)-[:BELONGS_TO]->(cat1)
CREATE (i3)-[:BELONGS_TO]->(cat1)
CREATE (i4)-[:BELONGS_TO]->(cat1)
CREATE (i5)-[:BELONGS_TO]->(cat2)
CREATE (i6)-[:BELONGS_TO]->(cat2)

// Замовлення
CREATE (o1:Order {id: "order1", date: "2025-05-01"})
CREATE (o2:Order {id: "order2", date: "2025-05-03"})
CREATE (o3:Order {id: "order3", date: "2025-05-05"})
CREATE (o4:Order {id: "order4", date: "2025-05-06"})

// Покупки
CREATE (c1)-[:BOUGHT]->(o1)
CREATE (c1)-[:BOUGHT]->(o2)
CREATE (c2)-[:BOUGHT]->(o3)
CREATE (c3)-[:BOUGHT]->(o4)

// Зв'язки замовлення → товари
CREATE (o1)-[:CONTAINS]->(i1)
CREATE (o1)-[:CONTAINS]->(i2)
CREATE (o2)-[:CONTAINS]->(i3)
CREATE (o2)-[:CONTAINS]->(i4)
CREATE (o3)-[:CONTAINS]->(i5)
CREATE (o3)-[:CONTAINS]->(i2)
CREATE (o4)-[:CONTAINS]->(i6)
CREATE (o4)-[:CONTAINS]->(i3)

// Перегляди товарів
CREATE (c1)-[:VIEWED]->(i1)
CREATE (c1)-[:VIEWED]->(i3)
CREATE (c2)-[:VIEWED]->(i2)
CREATE (c2)-[:VIEWED]->(i4)
CREATE (c3)-[:VIEWED]->(i5)
CREATE (c4)-[:VIEWED]->(i6)
CREATE (c5)-[:VIEWED]->(i1)
CREATE (c5)-[:VIEWED]->(i2)
CREATE (c5)-[:VIEWED]->(i3)

WITH o
//Знайти Items які входять в конкретний Order (за Order id) 
MATCH (o:Order {id: "order1"})-[:CONTAINS]->(i:Item)
RETURN i.name AS ItemName, i.price AS Price


//Підрахувати вартість конкретного Order 
MATCH (:Order {id: "order2"})-[:CONTAINS]->(i:Item)
RETURN SUM(i.price) AS TotalOrderPrice

//Знайти всі Orders конкретного Customer
MATCH (:Customer {id: "cust1"})-[:BOUGHT]->(o:Order)
RETURN o.id AS OrderID, o.date AS Date

//Знайти всі Items куплені конкретним Customer (через його Orders)
MATCH (c:Customer {id: "cust1"})-[:BOUGHT]->(:Order)-[:CONTAINS]->(i:Item)
RETURN DISTINCT i

//Знайти загальну кількість Items куплені конкретним Customer (через його Order)
MATCH (c:Customer {id: "cust1"})-[:BOUGHT]->(:Order)-[:CONTAINS]->(i:Item)
RETURN count(i) AS totalItemsBought

//Знайти для Customer на яку загальну суму він придбав товарів (через його Order)
MATCH (c:Customer {id: "cust1"})-[:BOUGHT]->(:Order)-[:CONTAINS]->(i:Item)
RETURN sum(i.price) AS totalSpent

//Знайті скільки разів кожен товар був придбаний, відсортувати за цим значенням
MATCH (:Order)-[:CONTAINS]->(i:Item)
RETURN i.name, count(*) AS timesBought
ORDER BY timesBought DESC

//Знайти всі Items переглянуті (view) конкретним Customer
MATCH (c:Customer {id: "cust1"})-[:VIEWED]->(i:Item)
RETURN i

//Знайти інші Items що купувались разом з конкретним Item (тобто всі Items що входять до Order-s разом з даними Item)
MATCH (targetItem:Item {id: "item1"})<-[:CONTAINS]-(order:Order)-[:CONTAINS]->(otherItems:Item)
WHERE otherItems.id <> targetItem.id
RETURN DISTINCT otherItems

//Знайти Customers які купили даний конкретний Item
MATCH (c:Customer)-[:BOUGHT]->(:Order)-[:CONTAINS]->(i:Item {id: "item1"})
RETURN DISTINCT c

//Знайти для певного Customer(а) товари, які він переглядав, але не купив
MATCH (c:Customer {id: "cust1"})-[:VIEWED]->(item:Item)
WHERE NOT EXISTS {
  MATCH (c)-[:BOUGHT]->(:Order)-[:CONTAINS]->(item)
}
RETURN item