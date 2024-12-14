class FactorialService
    def calculate(n)
      raise ArgumentError, "Input must be a non-negative integer" if n < 0
      (1..n).reduce(1, :*)
    end
  end
  