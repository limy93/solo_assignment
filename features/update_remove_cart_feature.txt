Feature: Update or Remove Product from Cart

  As a customer
  I want to update the quantity or remove products from my shopping cart
  So that I can change my order before checkout

  Scenario: Update product quantity in cart
    Given I am on the Cart page
    When I change the quantity of a product
    And I click the "Update" button
    Then I should see the cart updated with the new quantity

  Scenario: Remove a product from the cart
    Given I am on the Cart page
    When I click the "Remove" button for a product
    Then I should see that the product is no longer in the cart