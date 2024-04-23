Feature: Add Products to Cart
  As a logged-in user
  I want to be able to add products to my cart
  So that I can purchase them later

  Background:
    Given I am a registered user
    And I am logged in

  Scenario: Adding a product to the cart from the products listing page
    Given I am on the products listing page
    When I click the "Add to Cart" button for a product
    Then I should be redirected to the cart page and see the product has been added to my cart for later purchase