Feature: Listing Products
  As a visitor or user
  I want to see a list of available products
  So that I can choose products to purchase

  Scenario: Viewing the products list
    Given I am on the Products page
    Then I should see a list of products

  Scenario: Viewing the product details
    Given I am on the Products page
    When I click on the "View Details" button to look for more details
    Then I should see the details of the selected product