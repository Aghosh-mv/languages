# Factorial in EasyLang - so simple!

function factorial(n)
  if n equals 0 then
    return 1
  end
  return n * factorial(n - 1)
end

# Or use the "to" style:
to factorial2(n)
  when n is 0
    give back 1
  done
  give back n * factorial2(n - 1)
done

print factorial(5)
print factorial2(5)

# Even more natural:
print the value of factorial(10)
